from s2e2.error import ExpressionError
from s2e2.operators.operator_plus import OperatorPlus

import pytest


class TestOperatorPlus:

    def setup_class(self):
        self.operator = OperatorPlus()


    def teardown_class(self):
        self.operator = None


    def test_positive_good_arguments_stack_size(self):
        stack = ['A', 'B']
        self.operator.invoke(stack)
        assert len(stack) == 1


    def test_positive_good_arguments_result_type(self):
        stack = ['A', 'B']
        self.operator.invoke(stack)
        assert isinstance(stack[0], str)


    def test_positive_string_string_result_value(self):
        stack = ['A', 'B']
        self.operator.invoke(stack)
        assert stack[0] == 'AB'


    def test_positive_string_none_result_value(self):
        stack = ['A', None]
        self.operator.invoke(stack)
        assert stack[0] == 'A'


    def test_positive_none_string_result_value(self):
        stack = [None, 'B']
        self.operator.invoke(stack)
        assert stack[0] == 'B'


    def test_positive_none_none_result_value(self):
        stack = [None, None]
        self.operator.invoke(stack)
        assert stack[0] is None


    def test_positive_more_arguments_stack_size(self):
        stack = ['A', 'B', 'C']
        self.operator.invoke(stack)
        assert len(stack) == 2


    def test_negative_fewer_arguments(self):
        stack = ['A']
        with pytest.raises(ExpressionError) as ex:
            self.operator.invoke(stack)
        assert 'Not enough arguments' in str(ex.value)


    def test_negative_first_argument_wrong_type(self):
        stack = [5, 'B']
        with pytest.raises(ExpressionError) as ex:
            self.operator.invoke(stack)
        assert 'Invalid arguments' in str(ex.value)


    def test_negative_second_argument_wrong_type(self):
        stack = ['A', 5]
        with pytest.raises(ExpressionError) as ex:
            self.operator.invoke(stack)
        assert 'Invalid arguments' in str(ex.value)
