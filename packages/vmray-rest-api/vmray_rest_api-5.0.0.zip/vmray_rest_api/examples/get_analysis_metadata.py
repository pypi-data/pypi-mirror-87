#!/usr/bin/python3
"""Get VMRay Analyzer dynamic analysis metadata"""


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


def get_analysis_metadata(api, args):
    print("Getting analysis metadata for ID {}:".format(args.analysis_id))
    data = api.call("GET", "/rest/analysis/{}".format(args.analysis_id))

    print(json.dumps(data, indent=2))


def main():
    # set up argument parser
    parser = argparse.ArgumentParser(description="Get VMRay Analyzer dynamic analysis metadata")

    # arguments
    parser.add_argument("server", type=str, help="Server address")
    parser.add_argument("api_key", type=str, help="API key to use")
    parser.add_argument("--no_verify", "-n", action="store_true", help="Do not verify SSL certificate")

    parser.add_argument("analysis_id", type=int, help="Analysis ID")

    # parse args
    args = parser.parse_args()

    # create VMRay REST API object
    api = VMRayRESTAPI(args.server, args.api_key, not args.no_verify)

    # perform API call
    return get_analysis_metadata(api, args)


if __name__ == "__main__":
    main()
