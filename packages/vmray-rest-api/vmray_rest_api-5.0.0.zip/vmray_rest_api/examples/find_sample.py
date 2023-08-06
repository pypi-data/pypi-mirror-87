#!/usr/bin/python3
"""Find sample in VMRay database by SHA256 hash value"""


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


def find_sample(api, args):
    print("Finding samples with SHA256 " + args.sha256)
    data = api.call("GET", "/rest/sample/sha256/" + args.sha256)

    print("The following samples were found:")
    print(json.dumps(data, indent=2))


def main():
    # set up argument parser
    parser = argparse.ArgumentParser(description="Find sample in VMRay database by SHA256 hash value")

    # arguments
    parser.add_argument("server", type=str, help="Server address")
    parser.add_argument("api_key", type=str, help="API key to use")
    parser.add_argument("--no_verify", "-n", action="store_true", help="Do not verify SSL certificate")

    parser.add_argument("sha256", type=str, help="SHA256 hash value of sample")

    # parse args
    args = parser.parse_args()

    # create VMRay REST API object
    api = VMRayRESTAPI(args.server, args.api_key, not args.no_verify)

    # perform API call
    return find_sample(api, args)


if __name__ == "__main__":
    main()
