import os
import argparse
from robot.errors import DataError
from .suite_visitor.suite_visitor import SuiteStatus
from .test_visitor.test_visitor import TestStatus
from .utils.random_pipeline_id import *

os.chdir(os.path.dirname(__file__))


def cli():
    parser = argparse.ArgumentParser(
        prog='Robotframework XML report parser to JSON',
        description='This tool parses the robotframework output.xml result file, transforms into a JSON'
                    ' payload with suite and test metrics and send that to the REST API server or save locally.'
    )
    parser.add_argument('--inpath', dest='inpath', type=str, required=True,
                        help="path of the robotframework result xml file")
    parser.add_argument('--to-server', dest='server',
                        action='store_true', default=False, help="debug output to console")
    parser.add_argument('--to-console', dest='console',
                        action='store_true', default=False, help="debug output to console")
    parser.add_argument('--local', dest='local', action='store',
                        type=argparse.FileType('w', encoding='UTF-8'), help="save metrics file locally as JSON")
    parser_args = parser.parse_args()

    path = None

    if (parser_args.server and parser_args.console) or \
        (parser_args.server and parser_args.local) or \
            (parser_args.console and parser_args.local):
        print("Use only one output option at a time.")
        print("options: --to-server, --to-console or --local")
        return

    if parser_args.inpath and not parser_args.inpath.isspace():
        path = parser_args.inpath

    suites = get_suites(parser_args.inpath)
    payload = {**suites}

    tests = get_tests(parser_args.inpath)
    payload = {**suites, **tests}

    if parser_args.console:
        print(payload)
        return

    if parser_args.local:
        parser_args.local.write(str(payload))
        return

    if parser_args.server:
        # TODO: post payload to robot-parser API. Server not implemented yet.
        print('------------ to server')
        return


def get_suites(in_path):
    try:
        return SuiteStatus.get_suite_status(in_path)
    except DataError as e:
        raise Exception(f'No compatible XML file found in path. Error: {e}')


def get_tests(in_path):
    try:
        return TestStatus.get_test_status(in_path)
    except DataError as e:
        raise Exception(f'No compatible XML file found in path. Error: {e}')
