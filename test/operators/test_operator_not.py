from s2e2.error import ExpressionError
from s2e2.operators.operator_not import OperatorNot

import pytest


class TestOperatorNot:

    def setup_class(self):
        self.operator = OperatorNot()


    def teardown_class(self):
        self.operator = None


    def test_positive_good_arguments_stack_size(self):
        stack = [True]
        self.operator.invoke(stack)
        assert len(stack) == 1


    def test_positive_good_arguments_result_type(self):
        stack = [True]
        self.operator.invoke(stack)
        assert isinstance(stack[0], bool)


    def test_positive_argument_true_result_value(self):
        stack = [True]
        self.operator.invoke(stack)
        assert not stack[0]


    def test_positive_argument_false_result_value(self):
        stack = [False]
        self.operator.invoke(stack)
        assert stack[0]


    def test_positive_more_arguments_stack_size(self):
        stack = [False, False]
        self.operator.invoke(stack)
        assert len(stack) == 2


    def test_negative_fewer_arguments(self):
        stack = []
        with pytest.raises(ExpressionError) as ex:
            self.operator.invoke(stack)
        assert 'Not enough arguments' in str(ex.value)


    def test_negative_argument_wrong_type(self):
        stack = ['True']
        with pytest.raises(ExpressionError) as ex:
            self.operator.invoke(stack)
        assert 'Invalid arguments' in str(ex.value)


    def test_negative_argument_none(self):
        stack = [None]
        with pytest.raises(ExpressionError) as ex:
            self.operator.invoke(stack)
        assert 'Invalid arguments' in str(ex.value)
