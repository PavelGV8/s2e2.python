from s2e2.error import ExpressionError
from s2e2.operators.operator_equal import OperatorEqual

import pytest


class TestOperatorEqual:

    def setup_class(self):
        self.operator = OperatorEqual()


    def teardown_class(self):
        self.operator = None


    def test_positive_good_arguments_stack_size(self):
        stack = ['string1', 'string2']
        self.operator.invoke(stack)
        assert len(stack) == 1


    def test_positive_good_arguments_result_type(self):
        stack = ['string1', 'string2']
        self.operator.invoke(stack)
        assert isinstance(stack[0], bool)


    def test_positive_good_arguments_result_value(self):
        stack = ['string1', 'string1']
        self.operator.invoke(stack)
        assert stack[0]


    def test_positive_equal_strings_result_value(self):
        stack = ['string1', 'string1']
        self.operator.invoke(stack)
        assert stack[0]


    def test_positive_different_strings_result_value(self):
        stack = ['string1', 'string2']
        self.operator.invoke(stack)
        assert not stack[0]


    def test_positive_equal_integers_result_value(self):
        stack = [5, 5]
        self.operator.invoke(stack)
        assert stack[0]


    def test_positive_different_integers_result_value(self):
        stack = [5, 6]
        self.operator.invoke(stack)
        assert not stack[0]


    def test_positive_different_types_result_value(self):
        stack = [5, '5']
        self.operator.invoke(stack)
        assert not stack[0]


    def test_positive_first_argument_none_result_value(self):
        stack = [None, 'string']
        self.operator.invoke(stack)
        assert not stack[0]


    def test_positive_second_argument_none_result_value(self):
        stack = ['string', None]
        self.operator.invoke(stack)
        assert not stack[0]


    def test_positive_both_arguments_none_result_value(self):
        stack = [None, None]
        self.operator.invoke(stack)
        assert stack[0]


    def test_positive_more_arguments_stack_size(self):
        stack = ['string1', 'string2', 'string3']
        self.operator.invoke(stack)
        assert len(stack) == 2


    def test_negative_fewer_arguments(self):
        stack = ['string']
        with pytest.raises(ExpressionError) as ex:
            self.operator.invoke(stack)
        assert 'Not enough arguments' in str(ex.value)
