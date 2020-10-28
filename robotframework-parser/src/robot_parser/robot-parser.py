import argparse
from robot.errors import DataError
from .suite_visitor.suite_visitor import SuiteStatus
from .test_visitor.test_visitor import TestStatus
from .utils.random_pipeline_id import *

def cli():
    parser = argparse.ArgumentParser(
        prog='Robotframework XML report parser to JSON',
        description='This tool parses the robotframework output.xml result file, transforms into a JSON'
                    ' payload with suite and test metrics and send that to the REST API server or save locally.'
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--jenkins',  dest='jenkins', action='store_true', help="get jenkins pipeline's number")
    group.add_argument('--no-jenkins', dest='jenkins',  action='store_false', help="don't get jenkins pipeline 's number, use a random string instead")
    parser.add_argument('--metrics', dest='metrics',
                        choices=['suite', 'test', 'both'], default='both', help="select suite, test or both level metrics")
    parser.add_argument('--inpath', dest='inpath', required=True, help="path of the robotframework result xml file")
    parser.add_argument('--server', dest='server', required=True, help="server address to send parsed metrics")
    parser.add_argument('--to-console', dest='console',
                        action='store_true', default=False, help="debug output to console")
    parser.add_argument('--local', dest='local', action='store',
                        type=argparse.FileType('w', encoding='UTF-8'), help="save metrics file locall; tip: use json as file extension")
    parser_args = parser.parse_args()

    pipeline_id = ''
    payload = {}
    path = None

    if parser_args.jenkins:
        try:
            # TODO: method to get jenkins pipeline number
            pipeline_id = get_jenkins_pipeline_id()
        except Exception as e:
            print(f'Jenkins pipeline id not returned: {e}')
    else:
        try:
            pipeline_id = get_random_pipeline_id()
        except Exception as e:
            print(f'Random pipeline id not returned: {e}')

    if parser_args.inpath not in (None, ''):
        path = parser_args.inpath

    if parser_args.metrics == 'suite' and path and not parser_args.metrics == 'test':
        suites = get_suites(parser_args.inpath)
        payload = {**suites}
        payload['pipeline_id'] = pipeline_id
    elif (parser_args.metrics == 'test' and path and not parser_args.metrics == 'suite') or (parser_args.metrics == 'both' and path):
        suites = get_suites(parser_args.inpath)
        tests = get_tests(parser_args.inpath)
        payload = {**suites, **tests}
        payload['pipeline_id'] = pipeline_id

    if parser_args.server not in (None, ''):
        # TODO: webservice to do a POST to server
        pass

    if parser_args.console and payload not in (None, ''):
        print(payload)

    if parser_args.local and payload not in (None, ''):
        parser_args.local.write(str(payload))


def get_jenkins_pipeline_id():
    return ''


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
