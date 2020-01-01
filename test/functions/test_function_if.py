from s2e2.error import ExpressionError
from s2e2.functions.function_if import FunctionIf

import pytest


class TestFunctionIf:

    def setup_class(self):
        self.function = FunctionIf()


    def teardown_class(self):
        self.function = None


    def test_positive_good_arguments_stack_size(self):
        stack = [True, 'A', 'B']
        self.function.invoke(stack)
        assert len(stack) == 1


    def test_positive_good_arguments_result_type(self):
        stack = [True, 'A', 'B']
        self.function.invoke(stack)
        assert isinstance(stack[0], str)


    def test_positive_first_argument_true_result_value(self):
        stack = [True, 'A', 'B']
        self.function.invoke(stack)
        assert stack[0] == 'A'


    def test_positive_first_argument_false_result_value(self):
        stack = [False, 'A', 'B']
        self.function.invoke(stack)
        assert stack[0] == 'B'


    def test_positive_second_argument_none_result_value(self):
        stack = [True, None, 'B']
        self.function.invoke(stack)
        assert stack[0] is None


    def test_positive_third_argument_none_result_value(self):
        stack = [False, 'A', None]
        self.function.invoke(stack)
        assert stack[0] is None


    def test_positive_more_arguments_stack_size(self):
        stack = ['Arg', False, 'A', 'B']
        self.function.invoke(stack)
        assert len(stack) == 2


    def test_negative_fewer_arguments(self):
        stack = [False]
        with pytest.raises(ExpressionError) as ex:
            self.function.invoke(stack)
        assert 'Not enough arguments' in str(ex.value)


    def test_negative_first_argument_wrong_type(self):
        stack = ['False', 'A', 'B']
        with pytest.raises(ExpressionError) as ex:
            self.function.invoke(stack)
        assert 'Invalid arguments' in str(ex.value)


    def test_negative_first_argument_none(self):
        stack = [None, 'A', 'B']
        with pytest.raises(ExpressionError) as ex:
            self.function.invoke(stack)
        assert 'Invalid arguments' in str(ex.value)
