from ..utils.timezone_converter import *
from robot.api import ExecutionResult, ResultVisitor

tests_object = {}
test_list = []


class TestStatus(ResultVisitor):
    def start_test(self, test):
        global test_list
        object = {
            "parent": test.parent,
            "name": test.name,
            "longname": test.longname,
            "status": test.status,
            "message": test.message,
            "starttime": datetime_to_utc(test.starttime),
            "endtime": datetime_to_utc(test.endtime),
            "elapsed(s)": test.elapsedtime / float(1000),
        }
        test_list.append(object)

    @staticmethod
    def get_test_status(inpath):
        result = ExecutionResult(inpath)
        result.visit(TestStatus())
        tests_object["tests"] = test_list
        return tests_object
