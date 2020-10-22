import report_parser.test_visitor.test_visitor
import sys
from report_parser.test_visitor.test_visitor import TestStatus
from report_parser.suite_visitor.suite_visitor import SuiteStatus

if __name__ == "__main__":
    suite_list = SuiteStatus.get_suite_status(*sys.argv[1:])
    print(suite_list)
    test_object = TestStatus.get_test_status(*sys.argv[1:])
    print(test_object)
