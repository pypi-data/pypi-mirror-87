#!/usr/bin/python3
"""Get all running VMRay Analyzer jobs"""


import argparse
import json
import os
import sys


FILE = os.path.abspath(os.path.realpath(__file__))


try:
    # try to import VMRay REST API
    from vmray.rest_api import VMRayRESTAPI
except ImportError:
    # if VMRAY REST API is not installed, try relative import
    sys.path.append(os.path.join(os.path.dirname(FILE), ".."))
    from vmray.rest_api import VMRayRESTAPI


def get_all_jobs(api):
    print("The following running jobs exist:")
    data = api.call("GET", "/rest/job")
    print(json.dumps(data, indent=2))


def main():
    # set up argument parser
    parser = argparse.ArgumentParser(description="Get all running VMRay Analyzer jobs")

    # arguments
    parser.add_argument("server", type=str, help="Server address")
    parser.add_argument("api_key", type=str, help="API key to use")
    parser.add_argument("--no_verify", "-n", action="store_true", help="Do not verify SSL certificate")

    # parse args
    args = parser.parse_args()

    # create VMRay REST API object
    api = VMRayRESTAPI(args.server, args.api_key, not args.no_verify)

    # perform API call
    return get_all_jobs(api)


if __name__ == "__main__":
    main()
