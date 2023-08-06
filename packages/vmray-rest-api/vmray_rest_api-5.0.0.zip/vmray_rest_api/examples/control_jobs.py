#!/usr/bin/python3
"""Control VMRay Analyzer jobs"""


import argparse
import os
import sys
import time

from datetime import datetime


FILE = os.path.abspath(os.path.realpath(__file__))


try:
    # try to import VMRay REST API
    from vmray.rest_api import VMRayRESTAPI
except ImportError:
    # if VMRAY REST API is not installed, try relative import
    sys.path.append(os.path.join(os.path.dirname(FILE), ".."))
    from vmray.rest_api import VMRayRESTAPI


def set_min_prio(api, priority):
    vmhosts = api.call("GET", "/rest/vmhost")
    for vmhost in vmhosts:
        vmhosts = api.call("POST", "/rest/vmhost/{}".format(vmhost["vmhost_id"]), {"vmhost_minpriority": priority})


def wait_empty_queue(api, timeout):
    start = datetime.now()

    while api.call("GET", "/rest/job"):
        if timeout is not None and (datetime.now() - start).seconds >= timeout:
            raise Exception("Timed out while waiting for empty queue")

        time.sleep(1)


def wait_inwork_queue(api, timeout):
    start = datetime.now()

    while api.call("GET", "/rest/job/status/inwork"):
        if timeout is not None and (datetime.now() - start).seconds >= timeout:
            raise Exception("Timed out while waiting for inwork queue")

        time.sleep(1)


def main():
    # set up argument parser
    parser = argparse.ArgumentParser(description="Control VMRay Analyzer jobs")

    # arguments
    parser.add_argument("server", type=str, help="Server address")
    parser.add_argument("api_key", type=str, help="API key to use")
    parser.add_argument("--no_verify", "-n", action="store_true", help="Do not verify SSL certificate")

    # commands
    subparsers = parser.add_subparsers(dest="command")

    # set_min_prio
    set_min_prio_parser = subparsers.add_parser("set_min_prio",
                                                help="Set minimum priority of the jobs that are handled "
                                                "(for all connected VMRay Analyzer worker)")
    set_min_prio_parser.add_argument("priority", type=int, help="Priority to set")

    # wait_empty_queue
    wait_empty_queue_parser = subparsers.add_parser("wait_empty_queue",
                                                    help="Wait until VMRay Analyzer job queue is empty")
    wait_empty_queue_parser.add_argument("--timeout", "-t", type=int, default=None,
                                         help="Maximum number of seconds to wait")

    # wait_inwork_queue
    wait_inwork_queue_parser = subparsers.add_parser("wait_inwork_queue",
                                                     help="Wait until VMRay Analyzer job queue "
                                                     "has no more inwork items")
    wait_inwork_queue_parser.add_argument("--timeout", "-t", type=int, default=None,
                                          help="Maximum number of seconds to wait")

    # parse args
    args = parser.parse_args()

    # create VMRay REST API object
    api = VMRayRESTAPI(args.server, args.api_key, not args.no_verify)

    # execute command
    if args.command == "set_min_prio":
        set_min_prio(api, args.priority)
    elif args.command == "wait_empty_queue":
        wait_empty_queue(api, args.timeout)
    elif args.command == "wait_inwork_queue":
        wait_inwork_queue(api, args.timeout)


if __name__ == "__main__":
    main()
