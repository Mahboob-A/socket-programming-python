import socket
import sys
import logging
from time import sleep
import threading

from config import (
    NUMBER_OF_THREADS,
    JOB_NUMBER,
    Q,
)
from server import (
    handle_connections,
    handle_command_communications,
)
from utils import stop_event

### workers
def create_workers():
    """Creates threads for handling server."""
    for _ in range(NUMBER_OF_THREADS):
        t = threading.Thread(target=handle_works)
        t.daemon = True  # stop the thread when the program has stopped
        t.start()


def create_jobs():
    """Initilizes the queue with numeric values to indetify the workers."""
    for job_number in JOB_NUMBER:
        # 1, and 2.
        Q.put(job_number)

    Q.join()


def handle_works():
    """Handles workers duties."""
    global stop_event 
    while not stop_event.is_set():
        worker = Q.get()

        if worker == 1:
            handle_connections()
        elif worker == 2:
            handle_command_communications()

        Q.task_done()


def main(): 
    ''' Main entrypoint of the program. '''
    logging.basicConfig(level=logging.INFO)
    logging.info("Starting server...")

    create_workers()
    create_jobs()


if __name__ == '__main__': 
        main()
