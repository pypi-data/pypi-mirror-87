#!/usr/bin/python3
"""Mass download samples from VMRay Analyzer"""


import argparse
import io
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


def mass_download_samples(api, args):
    print("Downloading samples")
    hashes = [value.strip() for value in args.filename.readlines()]

    for sha256 in hashes:
        # get sample ID
        samples = api.call("GET", "/rest/sample/sha256/" + sha256)
        if not samples:
            print("Warning: No sample with sha256 \"{}\" found in VMRay Analyzer".format(sha256))
            continue

        # get sample file
        data = api.call("GET", "/rest/sample/{}/file".format(samples[0]["sample_id"]), raw_data=True)

        # write to disk
        with io.open(os.path.join(args.target_dir, sha256 + ".zip"), "wb") as fobj:
            fobj.write(data.read())

    print("Done. Samples are saved as ZIP archives and the password is always \"infected\".")


def main():
    # set up argument parser
    parser = argparse.ArgumentParser(description="Mass download samples from VMRay Analyzer")

    # arguments
    parser.add_argument("server", type=str, help="Server address")
    parser.add_argument("api_key", type=str, help="API key to use")
    parser.add_argument("--no_verify", "-n", action="store_true", help="Do not verify SSL certificate")

    parser.add_argument("filename", type=argparse.FileType("r"),
                        help="File which contains SHA256 hashes of samples "
                        "that should be downloaded (one hash per line)")
    parser.add_argument("target_dir", type=str, help="Target directory in which to save downloaded samples")

    # parse args
    args = parser.parse_args()

    # create VMRay REST API object
    api = VMRayRESTAPI(args.server, args.api_key, not args.no_verify)

    # perform API call
    return mass_download_samples(api, args)


if __name__ == "__main__":
    main()
