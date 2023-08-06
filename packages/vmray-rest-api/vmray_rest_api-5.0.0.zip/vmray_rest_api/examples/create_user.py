#!/usr/bin/python3
"""Create a new user in VMRay Analyzer database"""


import argparse
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


def create_user(api, args):
    print("Creating new user with e-mail \"{}\"".format(args.email))

    # update data
    api.call("POST", "/rest/user", params={
        "user_email": args.email,
        "user_password": args.password,
        "user_company": args.company,
        "user_first_name": args.first_name,
        "user_last_name": args.last_name,
        "user_submission_sampleset_id": 0,
    })


def main():
    # set up argument parser
    parser = argparse.ArgumentParser(description="Create a new user in VMRay Analyzer database")

    # arguments
    parser.add_argument("server", type=str, help="Server address")
    parser.add_argument("api_key", type=str, help="API key to use")
    parser.add_argument("--no_verify", "-n", action="store_true", help="Do not verify SSL certificate")

    parser.add_argument("email", type=str, help="Email address")
    parser.add_argument("password", type=str, help="Password")
    parser.add_argument("company", type=str, help="Company")
    parser.add_argument("first_name", type=str, help="First name")
    parser.add_argument("last_name", type=str, help="Last name")

    # parse args
    args = parser.parse_args()

    # create VMRay REST API object
    api = VMRayRESTAPI(args.server, args.api_key, not args.no_verify)

    # perform API call
    return create_user(api, args)


if __name__ == "__main__":
    main()
