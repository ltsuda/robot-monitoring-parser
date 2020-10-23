from robot.api import ExecutionResult, ResultVisitor

test_object = []


class TestStatus(ResultVisitor):

    def start_test(self, test):
        global test_object
        object = {
            'parent': test.parent,
            'name': test.name,
            'status': test.status,
            'starttime': test.starttime,
            'endtime': test.endtime,
            'elapsed(s)': test.elapsedtime/float(1000)
        }
        test_object.append(object)

    @staticmethod
    def get_test_status(inpath):
        result = ExecutionResult(inpath)
        result.visit(TestStatus())
        return test_object
