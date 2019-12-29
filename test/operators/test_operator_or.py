from s2e2.error import ExpressionError
from s2e2.operators.operator_or import OperatorOr

import pytest


class TestOperatorOr:

    def setup_class(self):
        self.operator = OperatorOr()


    def teardown_class(self):
        self.operator = None


    def test_positive_good_arguments_stack_size(self):
        stack = [True, True]
        self.operator.invoke(stack)
        assert len(stack) == 1


    def test_positive_good_arguments_result_type(self):
        stack = [True, True]
        self.operator.invoke(stack)
        assert isinstance(stack[0], bool)


    def test_positive_true_true_result_value(self):
        stack = [True, True]
        self.operator.invoke(stack)
        assert stack[0]


    def test_positive_true_false_result_value(self):
        stack = [True, False]
        self.operator.invoke(stack)
        assert stack[0]


    def test_positive_false_true_result_value(self):
        stack = [False, True]
        self.operator.invoke(stack)
        assert stack[0]


    def test_positive_false_false_result_value(self):
        stack = [False, False]
        self.operator.invoke(stack)
        assert not stack[0]


    def test_positive_more_arguments_stack_size(self):
        stack = ['Arg', False, True]
        self.operator.invoke(stack)
        assert len(stack) == 2


    def test_negative_fewer_arguments(self):
        stack = [False]
        with pytest.raises(ExpressionError) as ex:
            self.operator.invoke(stack)
        assert 'Not enough arguments' in str(ex.value)


    def test_negative_first_argument_wrong_type(self):
        stack = ['True', False]
        with pytest.raises(ExpressionError) as ex:
            self.operator.invoke(stack)
        assert 'Invalid arguments' in str(ex.value)


    def test_negative_first_argument_none(self):
        stack = [None, False]
        with pytest.raises(ExpressionError) as ex:
            self.operator.invoke(stack)
        assert 'Invalid arguments' in str(ex.value)


    def test_negative_second_argument_wrong_type(self):
        stack = [True, 'False']
        with pytest.raises(ExpressionError) as ex:
            self.operator.invoke(stack)
        assert 'Invalid arguments' in str(ex.value)


    def test_negative_second_argument_none(self):
        stack = [True, None]
        with pytest.raises(ExpressionError) as ex:
            self.operator.invoke(stack)
        assert 'Invalid arguments' in str(ex.value)
