from s2e2.error import ExpressionError
from s2e2.functions.function_now import FunctionNow

import datetime


class TestFunctionNow:

    def setup_class(self):
        self.function = FunctionNow()


    def teardown_class(self):
        self.function = None


    def test_positive_stack_size(self):
        stack = []
        self.function.invoke(stack)
        assert len(stack) == 1


    def test_positive_result_type(self):
        stack = []
        self.function.invoke(stack)
        assert isinstance(stack[0], datetime.datetime)


    def test_positive_result_value(self):
        stack = []
        self.function.invoke(stack)

        now = datetime.datetime.utcnow()
        function_result = stack[0]
        MAX_DIFF_IN_SECONDS = 2

        assert now >= function_result
        assert (now - function_result).seconds < MAX_DIFF_IN_SECONDS


    def test_positive_more_arguments_stack_size(self):
        stack = [False, 'A', 'B']
        self.function.invoke(stack)
        assert len(stack) == 4
