from s2e2.error import ExpressionError
from s2e2.functions.function_replace import FunctionReplace

import pytest


class TestFunctionReplace:

    def setup_class(self):
        self.function = FunctionReplace()


    def teardown_class(self):
        self.function = None


    def test_positive_good_arguments_stack_size(self):
        stack = ['ABA', 'A', 'B']
        self.function.invoke(stack)
        assert len(stack) == 1


    def test_positive_good_arguments_result_type(self):
        stack = ['ABA', 'A', 'B']
        self.function.invoke(stack)
        assert isinstance(stack[0], str)


    def test_positive_string_replace_result_value(self):
        stack = ['ABA', 'A', 'B']
        self.function.invoke(stack)
        assert stack[0] == 'BBB'


    def test_positive_regex_replace_result_value(self):
        stack = ['ABCABA', 'A.*?C', 'D']
        self.function.invoke(stack)
        assert stack[0] == 'DABA'


    def test_positive_special_symbol_replace_result_value(self):
        stack = ['A * B == C', '\\*', '+']
        self.function.invoke(stack)
        assert stack[0] == 'A + B == C'


    def test_positive_first_argument_none_result_value(self):
        stack = [None, 'A', 'B']
        self.function.invoke(stack)
        assert stack[0] is None


    def test_positive_first_argument_empty_string_result_value(self):
        stack = ['', 'A', 'B']
        self.function.invoke(stack)
        assert stack[0] == ''


    def test_positive_third_argument_empty_string_result_value(self):
        stack = ['ABA', 'B', '']
        self.function.invoke(stack)
        assert stack[0] == 'AA'


    def test_positive_more_arguments_stack_size(self):
        stack = [False, 'ABA', 'A', 'B']
        self.function.invoke(stack)
        assert len(stack) == 2


    def test_negative_fewer_arguments(self):
        stack = ['ABA', 'A']
        with pytest.raises(ExpressionError) as ex:
            self.function.invoke(stack)
        assert 'Not enough arguments' in str(ex.value)


    def test_negative_first_argument_wrong_type(self):
        stack = [5, 'A', 'B']
        with pytest.raises(ExpressionError) as ex:
            self.function.invoke(stack)
        assert 'Invalid arguments' in str(ex.value)


    def test_negative_second_argument_empty_string(self):
        stack = ['ABA', '', 'B']
        with pytest.raises(ExpressionError) as ex:
            self.function.invoke(stack)
        assert 'Invalid arguments' in str(ex.value)


    def test_negative_second_argument_none(self):
        stack = ['ABA', None, 'B']
        with pytest.raises(ExpressionError) as ex:
            self.function.invoke(stack)
        assert 'Invalid arguments' in str(ex.value)


    def test_negative_second_argument_wrong_type(self):
        stack = ['ABA', 5, 'B']
        with pytest.raises(ExpressionError) as ex:
            self.function.invoke(stack)
        assert 'Invalid arguments' in str(ex.value)


    def test_negative_third_argument_none(self):
        stack = ['ABA', 'A', None]
        with pytest.raises(ExpressionError) as ex:
            self.function.invoke(stack)
        assert 'Invalid arguments' in str(ex.value)


    def test_negative_third_argument_wrong_type(self):
        stack = ['ABA', 'A', 5]
        with pytest.raises(ExpressionError) as ex:
            self.function.invoke(stack)
        assert 'Invalid arguments' in str(ex.value)
