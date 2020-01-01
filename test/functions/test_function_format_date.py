from s2e2.error import ExpressionError
from s2e2.functions.function_format_date import FunctionFormatDate

import datetime
import pytest


class TestFunctionFormatDate:

    def setup_class(self):
        self.function = FunctionFormatDate()


    def teardown_class(self):
        self.function = None


    def test_positive_good_arguments_stack_size(self):
        stack = [datetime.datetime.utcnow(), '%Y-%m-%d']
        self.function.invoke(stack)
        assert len(stack) == 1


    def test_positive_good_arguments_result_type(self):
        stack = [datetime.datetime.utcnow(), '%Y-%m-%d']
        self.function.invoke(stack)
        assert isinstance(stack[0], str)


    def test_positive_good_arguments_result_value(self):
        first_argument = datetime.datetime(2019, 7, 13, 12, 15, 0, 0, datetime.timezone.utc)
        stack = [first_argument, '%Y-%m-%d']
        self.function.invoke(stack)
        assert stack[0] == '2019-07-13'


    def test_positive_second_argument_wrong_value(self):
        stack = [datetime.datetime.utcnow(), 'year-month-day']
        self.function.invoke(stack)
        assert stack[0] == 'year-month-day'


    def test_positive_more_arguments_stack_size(self):
        stack = [False, datetime.datetime.utcnow(), '%Y-%m-%d']
        self.function.invoke(stack)
        assert len(stack) == 2


    def test_negative_fewer_arguments(self):
        stack = [datetime.datetime.utcnow()]
        with pytest.raises(ExpressionError) as ex:
            self.function.invoke(stack)
        assert 'Not enough arguments' in str(ex.value)


    def test_negative_first_argument_wrong_type(self):
        stack = ['2019-07-13', '%Y-%m-%d']
        with pytest.raises(ExpressionError) as ex:
            self.function.invoke(stack)
        assert 'Invalid arguments' in str(ex.value)


    def test_negative_first_argument_none(self):
        stack = [None, '%Y-%m-%d']
        with pytest.raises(ExpressionError) as ex:
            self.function.invoke(stack)
        assert 'Invalid arguments' in str(ex.value)


    def test_negative_second_argument_wrong_type(self):
        stack = [datetime.datetime.utcnow(), 15]
        with pytest.raises(ExpressionError) as ex:
            self.function.invoke(stack)
        assert 'Invalid arguments' in str(ex.value)


    def test_negative_second_argument_none(self):
        stack = [datetime.datetime.utcnow(), None]
        with pytest.raises(ExpressionError) as ex:
            self.function.invoke(stack)
        assert 'Invalid arguments' in str(ex.value)
       