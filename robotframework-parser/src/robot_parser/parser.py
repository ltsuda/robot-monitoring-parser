import sys
from .suite_visitor.suite_visitor import SuiteStatus
from .test_visitor.test_visitor import TestStatus

def main():
    suite_list = SuiteStatus.get_suite_status(*sys.argv[1:])
    print(suite_list)
    test_object = TestStatus.get_test_status(*sys.argv[1:])
    print(test_object)
