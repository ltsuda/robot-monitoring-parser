from ..utils.timezone_converter import *
from robot.api import ExecutionResult, ResultVisitor

suites_object = {}
suite_list = []


class SuiteStatus(ResultVisitor):
    def start_suite(self, suite):
        global suite_list
        stats = suite.statistics
        object = {
            "name": suite,
            "longname": suite.longname,
            "status": suite.status,
            "total": stats.all.total,
            "passed": stats.all.passed,
            "failed": stats.all.failed,
            "starttime": datetime_to_utc(suite.starttime),
            "endtime": datetime_to_utc(suite.endtime),
            "elapsed(s)": suite.elapsedtime / float(1000),
        }
        suite_list.append(object)

    @staticmethod
    def get_suite_status(inpath):
        result = ExecutionResult(inpath)
        result.visit(SuiteStatus())
        suites_object["suites"] = suite_list
        return suites_object
