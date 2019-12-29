from s2e2.error import ExpressionError
from s2e2.functions.function_add_days import FunctionAddDays

import datetime
import pytest


class TestFunctionAddDays:

    def setup_class(self):
        self.function = FunctionAddDays()


    def teardown_class(self):
        self.function = None


    def test_positive_good_arguments_stack_size(self):
        stack = [datetime.datetime.utcnow(), '1']
        self.function.invoke(stack)
        assert len(stack) == 1


    def test_positive_good_arguments_result_type(self):
        stack = [datetime.datetime.utcnow(), '1']
        self.function.invoke(stack)
        assert isinstance(stack[0], datetime.datetime)


    def test_positive_second_argument_positive_result_value(self):
        first_argument = datetime.datetime(2019, 7, 13, 12, 15, 0, 0, datetime.timezone.utc)
        stack = [first_argument, '1']

        self.function.invoke(stack)

        function_result = stack[0]
        assert (function_result - first_argument).days == 1


    def test_positive_second_argument_zero_result_value(self):
        first_argument = datetime.datetime(2019, 7, 13, 12, 15, 0, 0, datetime.timezone.utc)
        stack = [first_argument, '0']

        self.function.invoke(stack)

        function_result = stack[0]
        assert function_result == first_argument


    def test_positive_second_argument_negative_result_value(self):
        first_argument = datetime.datetime(2019, 7, 13, 12, 15, 0, 0, datetime.timezone.utc)
        stack = [first_argument, '-1']

        self.function.invoke(stack)

        function_result = stack[0]
        assert (first_argument - function_result).days == 1


    def test_positive_second_argument_integer_result_value(self):
        first_argument = datetime.datetime(2019, 7, 13, 12, 15, 0, 0, datetime.timezone.utc)
        stack = [first_argument, 1]

        self.function.invoke(stack)

        function_result = stack[0]
        assert (function_result - first_argument).days == 1


    def test_positive_more_arguments_stack_size(self):
        stack = ['Arg', datetime.datetime.utcnow(), '1']
        self.function.invoke(stack)
        assert len(stack) == 2


    def test_negative_fewer_arguments(self):
        stack = [datetime.datetime.utcnow()]
        with pytest.raises(ExpressionError) as ex:
            self.function.invoke(stack)
        assert 'Not enough arguments' in str(ex.value)


    def test_negative_first_argument_wrong_type(self):
        stack = ['2019-07-13 00:00:00', '1']
        with pytest.raises(ExpressionError) as ex:
            self.function.invoke(stack)
        assert 'Invalid arguments' in str(ex.value)


    def test_negative_first_argument_none(self):
        stack = [None, '1']
        with pytest.raises(ExpressionError) as ex:
            self.function.invoke(stack)
        assert 'Invalid arguments' in str(ex.value)


    def test_negative_second_argument_none(self):
        stack = [datetime.datetime.utcnow(), None]
        with pytest.raises(ExpressionError) as ex:
            self.function.invoke(stack)
        assert 'Invalid arguments' in str(ex.value)


    def test_negative_second_argument_wrong_value(self):
        stack = [datetime.datetime.utcnow(), 'A']
        with pytest.raises(ExpressionError) as ex:
            self.function.invoke(stack)
        assert 'Invalid arguments' in str(ex.value)
