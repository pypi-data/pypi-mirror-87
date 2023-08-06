import google.api_core.exceptions
import google.cloud.logging
import google.cloud.pubsub_v1
import google.cloud.storage
import json
import logging
import os
import requests
import subprocess
import tempfile
import threading
import time


def run():
    """
    Read and process messages from the subscription $GCE_SUBSCRIPTION by running each as a script.

    This is the primary entry point for the script.

    :return: None
    """

    # Initialize logging
    logging_client = google.cloud.logging.Client()
    logging_client.setup_logging()
    hostname = requests.get(
        "http://metadata.google.internal/computeMetadata/v1/instance/name",
        headers={"Metadata-Flavor": "Google"},
    ).text
    logger = Logger(hostname)

    try:
        process_messages(
            os.getenv("GCE_SUBSCRIPTION"), int(os.getenv("RETRY_DELAY", 0)), logger
        )
    except Exception as e:
        # Continue the shutdown on any error
        logger.error(e)

    try:
        kill_vm(logger)
    except Exception as e:
        # Log the error and admit defeat
        logger.error(e)


def process_messages(subscription_path, delay_poll_if_empty, logger):
    """
    Read and process messages from the provided subscription. If [delay_poll_if_empty] is 0, then
    exit when the subscription is empty; otherwise, retry after waiting [delay_poll_if_empty] seconds.

    :param subscription_path: The subscription to read messages from.
    :param delay_poll_if_empty: Time to wait between reads of an empty subscription (seconds).
    :param logger: Log writer to use
    :return: None
    """

    subscriber = google.cloud.pubsub_v1.SubscriberClient()
    storage_client = google.cloud.storage.Client()
    current_message = None
    running = True

    logger.info("Starting heartbeat thread")

    # Every 30 seconds, request an extension on the currently active message
    def heartbeat():
        time.sleep(30)
        while running:
            local_msg = current_message
            if local_msg is not None:
                subscriber.modify_ack_deadline(
                    request={
                        "subscription": subscription_path,
                        "ack_ids": [local_msg.ack_id],
                        "ack_deadline_seconds": 60,
                    }
                )
            time.sleep(30)

    heartbeat_thread = threading.Thread(target=heartbeat, daemon=True)
    heartbeat_thread.start()

    logger.info("Looking for tasks in queue")
    while True:
        try:
            response = subscriber.pull(
                request={"subscription": subscription_path, "max_messages": 1}
            )
        except google.api_core.exceptions.DeadlineExceeded:
            if delay_poll_if_empty > 0:
                logger.info(
                    "0 tasks in queue. Sleeping for {delay} s".format(
                        delay=delay_poll_if_empty
                    )
                )
                time.sleep(delay_poll_if_empty)
                continue
            else:
                logger.info("0 tasks in queue. Worker will terminate.")
                running = False
                break

        for msg in response.received_messages:
            current_message = msg
            msg_logger = logger.add_context(msg.message.message_id)

            msg_logger.info(msg)
            try:
                process(msg, storage_client, msg_logger)
            except Exception as e:
                msg_logger.error(e)
            subscriber.acknowledge(
                request={"subscription": subscription_path, "ack_ids": [msg.ack_id]}
            )
            current_message = None


def process(msg, storage_client, logger):
    """
    Process a single message by running it as a script.

    If directed by the message, this function will also download/upload files from/to GCS.

    :param msg: The message to process.
    :param storage_client: The client for interacting with GCS.
    :param logger: Log writer to use
    :return: None
    """
    with tempfile.TemporaryDirectory() as local:
        # Write the message text to a file
        message_script_path = local + "/message.sh"
        with open(message_script_path, "w") as message_script:
            message_script.write(msg.message.data.decode("utf-8"))

        # Prepare the file structure for the message by copying from storage
        for command, blob_url in msg.message.attributes.items():
            if len(command) > 7 and command[:7] == "SOURCE ":
                blob = google.cloud.storage.Blob.from_string(
                    blob_url, client=storage_client
                )
                local_filename = local + "/" + command[7:]

                # Prepare the appropriate folder for the remote file
                if not os.path.exists(os.path.dirname(local_filename)):
                    os.makedirs(os.path.dirname(local_filename))
                blob.download_to_filename(local_filename)

        # Run the message
        subprocess.run(["chmod", "+x", message_script_path])
        result = subprocess.run(
            [message_script_path],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            cwd=local,
        )
        logger.info("[STDOUT] " + str(result.stdout))
        logger.info("[STDERR] " + str(result.stderr))

        # Copy any results to storage
        for command, blob_url in msg.message.attributes.items():
            if len(command) > 7 and command[:7] == "UPLOAD ":
                upload_files(storage_client, local + "/" + command[7:], blob_url)


def upload_files(storage_client, local_name, blob_url):
    """
    Upload [local_name] to google cloud storage at [blob_url].

    :param storage_client: The storage client to use for the upload.
    :param local_name: The local file or directory to upload.
    :param blob_url: The destination google cloud storage identifier.
    :return: None
    """
    if os.path.isfile(local_name):
        blob = google.cloud.storage.Blob.from_string(blob_url, client=storage_client)
        blob.upload_from_filename(local_name)
    elif os.path.isdir(local_name):
        for item in os.listdir(local_name):
            upload_files(storage_client, local_name + "/" + item, blob_url + "/" + item)


def kill_vm(logger):
    """
    If we are running inside of a GCE VM, kill it. If this VM is a part of a managed instance group,
    attempt to remove ourselves from the group (so that the instance group does not restart the VM).

    Based on https://stackoverflow.com/q/52748332/321772

    :param logger: Log writer to use
    :return: None
    """

    # Load the access token
    r = json.loads(
        requests.get(
            "http://metadata.google.internal/computeMetadata/v1/instance/service-accounts/default/token",
            headers={"Metadata-Flavor": "Google"},
        ).text
    )

    token = r["access_token"]

    # Load instance metadata (see https://cloud.google.com/compute/docs/storing-retrieving-metadata)
    project_id = requests.get(
        "http://metadata.google.internal/computeMetadata/v1/project/project-id",
        headers={"Metadata-Flavor": "Google"},
    ).text

    name = requests.get(
        "http://metadata.google.internal/computeMetadata/v1/instance/name",
        headers={"Metadata-Flavor": "Google"},
    ).text

    zone_long = requests.get(
        "http://metadata.google.internal/computeMetadata/v1/instance/zone",
        headers={"Metadata-Flavor": "Google"},
    ).text
    zone = zone_long.split("/")[-1]

    # First, try deleting from an instance group
    if "-" in name:
        # Guess our instance group name by following the instance naming convention.
        # Instance group instances appear to be named by "{instance_group}-[0-9a-z]*"
        # For example, "exp1-d-sf0l" is in the instance group "exp1-d".
        # I could not find an API to find the current instance group, but I think there should be.
        potential_instance_group = name[: name.rfind("-")]
        full_name = "https://www.googleapis.com/compute/v1/projects/{project}/zones/{zone}/instances/{name}".format(
            project=project_id, zone=zone, name=name
        )

        # Check if {full_name} appears in the managed instance group {potential_instance_group}
        instances = json.loads(
            requests.post(
                (
                    "https://compute.googleapis.com/compute/v1/projects/{project_id}/"
                    + "zones/{zone}/instanceGroupManagers/{resourceId}/listManagedInstances"
                ).format(
                    project_id=project_id,
                    zone=zone,
                    resourceId=potential_instance_group,
                ),
                # data={"filter": "name={name}".format(name=name)}, # Broken
                headers={"Authorization": "Bearer {token}".format(token=token)},
            ).text
        )

        # Filter is broken since 10/29/19 (https://issuetracker.google.com/issues/143463446) so filter by hand
        if "managedInstances" in instances:
            for instance in instances["managedInstances"]:
                if instance["instance"] == full_name:
                    # We found this VM! Delete it from the managed instance group
                    logger.info(
                        "Attempting to remove VM from instance group {instance_group}".format(
                            instance_group=potential_instance_group
                        )
                    )
                    requests.post(
                        "https://compute.googleapis.com/compute/v1/projects/{project}/zones/{zone}/instanceGroupManagers/{resourceId}/deleteInstances".format(
                            project=project_id,
                            zone=zone,
                            resourceId=potential_instance_group,
                        ),
                        data={
                            "instances": [
                                "zones/{zone}/instances/{name}".format(
                                    zone=zone, name=name
                                )
                            ]
                        },
                        headers={"Authorization": "Bearer {token}".format(token=token)},
                    )
                    return

        logger.info(
            "Unable to find VM in instance group {instance_group}".format(
                instance_group=potential_instance_group
            )
        )

    # If that fails, try deleting this VM directly
    logger.info("Deleting VM {zone}/{name} directly".format(zone=zone, name=name))
    requests.delete(
        "https://www.googleapis.com/compute/v1/projects/{project}/zones/{zone}/instances/{name}".format(
            project=project_id, zone=zone, name=name
        ),
        headers={"Authorization": "Bearer {token}".format(token=token)},
    )


class Logger:
    """
    A simple class to add context to a logging call.
    """

    def __init__(self, *prefixes):
        self._prefixes = prefixes
        self._message_prefix = ""
        for prefix in self._prefixes:
            self._message_prefix += "[" + prefix + "] "

    def info(self, msg):
        logging.info(self._message_prefix + str(msg))

    def error(self, msg):
        logging.error(self._message_prefix + str(msg))

    def add_context(self, *prefixes):
        return Logger(*self._prefixes, *prefixes)


if __name__ == "__main__":
    run()
