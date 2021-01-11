from __future__ import print_function

import argparse
import json
import os
import pathlib
import sys
from datetime import datetime
import pandas as pd

import numpy as np
from google.oauth2 import service_account
from googleapiclient import discovery

from .util import make_registration_decorator, make_logger, make_target_dir_from_path

logger = make_logger(__name__)
register_command, command_fns = make_registration_decorator()


def setup_export(subparser):
    subparser.add_argument("target_dir", type=str)


@register_command
def download_json(args):
    with open(args.credentials_path) as source:
        info = json.load(source)
        credentials = service_account.Credentials.from_service_account_info(info)
    service = discovery.build("sheets", "v4", credentials=credentials)
    request = (
        service.spreadsheets()
        .values()
        .get(spreadsheetId=args.googlesheets_id, range="A1:L1000")
    )

    response = request.execute()
    logger.info(f"response is: {response}")
    if not response or not response["values"]:
        raise Exception(
            "Unable to retrieve googlespreadsheets data from API, using spreadsheet_id: {0}".format(
                args.googlesheets_id
            )
        )
    # pandas allows us to see empty and blank values to convert to common value
    df = pd.DataFrame(response["values"])
    df_with_no_nulls = df.replace([None], [""])
    df_sanitised = df_with_no_nulls.replace(regex={r"\n": ","})
    processed_dataset = df_sanitised.values.tolist()
    # validate that data is a 2D array (or list of arrays)
    logger.info("Validating data as numpy data...")
    validate_as_numpy(processed_dataset)
    backup_exising_googlesheet(args)
    write_result_as_json(args, processed_dataset)


def backup_exising_googlesheet(args):
    if os.path.isfile(args.target_path):
        logger.info("Existing target path found. Validating...")
        result = open_valid_googlesheet_file(args.target_path)
        validate_as_numpy(result)
        logger.info(
            "Existing target path contains valid numpy data. Backing up file..."
        )
        # create backup path in its own 'backups' folder and filename using datetimestamp
        backup_path_ext_parts = os.path.splitext(args.target_path)
        backup_path_parts = os.path.split(backup_path_ext_parts[0])
        backup_dir = os.path.join(backup_path_parts[0], "backups")
        pathlib.Path(backup_dir).mkdir(parents=True, exist_ok=True)
        backup_path = os.path.join(
            backup_dir,
            backup_path_parts[1]
            + datetime.now().strftime("-%d%m%Y-%H%M%S")
            + backup_path_ext_parts[1],
        )
        os.rename(args.target_path, backup_path)
        logger.info(f"Existing target path successfully moved to {backup_path}")


def validate_as_numpy(data):
    valid_numpy = np.array(data)
    if valid_numpy is None:
        raise Exception("Data is not in a list of arrays format: {0}".format(data))


def write_result_as_json(args, json_data):
    with open(args.target_path, "w+") as destination:
        json.dump(json_data, destination)
    # show how data appears in written file
    results = open_valid_googlesheet_file(args.target_path)
    logger.info(
        f"Googlesheet data written to: {args.target_path} with results: {results}"
    )


def open_valid_googlesheet_file(path):
    with open(path) as valid_destination:
        return json.load(valid_destination)


def version():
    import pkg_resources

    version = pkg_resources.version
    print(
        """\
bpa-ckan-export, version %s

Copyright (C) 2020 Queensland Cyber Infrastructure Foundation (http://www.qcif.edu.au/)

(See LICENSE at: https://github.com/BioplatformsAustralia/bpa-googlesheets/blob/master/LICENSE)
"""
        % (version)
    )
    sys.exit(0)


def usage(parser):
    parser.print_usage()
    sys.exit(0)


def commands():
    for fn in command_fns:
        name = fn.__name__.replace("_", "-")
        yield name, fn, fn.__doc__


def main():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument("--version", action="store_true", help="print version and exit")
    parser.add_argument(
        "-c",
        "--credentials-path",
        help="credentials json file for accessing googlesheets API",
        default="/opt/Bioplatforms-googlesheet-credentials.json",
    )
    parser.add_argument("-i", "--googlesheets-id", help="googlsheets ID")
    parser.add_argument(
        "-t",
        "--target-path",
        help="target path to download json to",
        default="/tmp/googlesheets/summary_table_data_path.json",
    )

    subparsers = parser.add_subparsers(dest="name")
    for name, fn, help_text in sorted(commands()):
        subparser = subparsers.add_parser(name, help=help_text)
        subparser.set_defaults(func=fn)
        setup_export(subparser)
    args = parser.parse_args()
    if args.version:
        version()
    if "func" not in args:
        args.func = download_json
    make_target_dir_from_path(args.credentials_path)
    make_target_dir_from_path(args.target_path)
    args.func(args)
