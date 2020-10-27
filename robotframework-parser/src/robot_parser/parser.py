import sys

from robot.errors import DataError
from .suite_visitor.suite_visitor import SuiteStatus
from .test_visitor.test_visitor import TestStatus
from .utils.random_pipeline_id import *

def main():
    # TODO: method to get jenkins pipeline number
    jenkins = False
    pipeline_id = None
    if jenkins is True:
        pass
    else:
        try:
            pipeline_id = get_random_pipeline_id()
        except Exception as e:
            print(f'Random pipeline id not returned: {e}')

    suites = get_suites(*sys.argv[1:])
    suites['pipeline_id'] = pipeline_id
    print(suites)
    tests = get_tests(*sys.argv[1:])
    tests['pipeline_id'] = pipeline_id
    print(tests)
    # TODO: webservice to do a POST to server

def get_suites(in_path):
    try:
        return SuiteStatus.get_suite_status(in_path)
    except DataError as e:
        print(f'No compatible XML file found in path. Error: {e}')

def get_tests(in_path):
    try:
        return TestStatus.get_test_status(in_path)
    except DataError as e:
        print(f'No compatible XML file found in path. Error: {e}')


# --help
# --jenkins bool, default True when server/DB are done. For now, False
# --filePath
# --metrics suite or tests or both. If select only tests, force include suite
# --debug bool
# --debugPath if debug selected, save JSON locally or print on console
# --version