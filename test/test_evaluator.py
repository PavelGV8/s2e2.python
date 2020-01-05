from s2e2.converter import Converter
from s2e2.error import ExpressionError
from s2e2.evaluator import Evaluator
from s2e2.token_type import TokenType
from s2e2.token import Token
from s2e2.tokenizer import Tokenizer

from s2e2.functions.function import Function
from s2e2.operators.operator import Operator

import mock
import pytest


class TestEvaluator:

    class DummyFunction(Function):
        def __init__(self):
            super().__init__('Function', 2)

        def _check_arguments(self):
            return True

        def _result(self):
            return 'FunctionResult'


    class DummyOperator(Operator):
        def __init__(self):
            super().__init__('Operator', 1, 2)

        def _check_arguments(self):
            return True

        def _result(self):
            return 'OperatorResult'


    def setup(self):
        self.evaluator = Evaluator()


    def teardown(self):
        self.evaluator = None


    def test_positive_nothing_added_supported_functions_size(self):
        assert len(self.evaluator.get_functions()) == 0


    def test_positive_nothing_added_supported_operators_size(self):
        assert len(self.evaluator.get_operators()) == 0


    def test_positive_nothing_added_evaluation_result(self):
        input_expression = 'A B C'
        output_expression = self.evaluator.evaluate(input_expression)
        assert input_expression == output_expression


    def test_positive_add_function_supported_functions_size(self):
        self.evaluator.add_function(TestEvaluator.DummyFunction())
        assert len(self.evaluator.get_functions()) == 1


    def test_positive_add_function_verify_tokenizer(self):
        tokenizer_mock = mock.Mock(spec=Tokenizer)
        self.evaluator = Evaluator.mocked(None, tokenizer_mock)

        dummy_function = TestEvaluator.DummyFunction()
        self.evaluator.add_function(dummy_function)

        tokenizer_mock.add_function.assert_called_once_with(dummy_function.name)


    def test_positive_add_operator_supported_operators_size(self):
        self.evaluator.add_operator(TestEvaluator.DummyOperator())
        assert len(self.evaluator.get_operators()) == 1


    def test_positive_add_operator_verify_converter(self):
        converter_mock = mock.Mock(spec=Converter)
        tokenizer_mock = mock.Mock(spec=Tokenizer)
        self.evaluator = Evaluator.mocked(converter_mock, tokenizer_mock)

        dummy_operator = TestEvaluator.DummyOperator()
        self.evaluator.add_operator(dummy_operator)

        converter_mock.add_operator.assert_called_once_with(dummy_operator.name, dummy_operator.priority)


    def test_positive_add_operator_verify_tokenizer(self):
        converter_mock = mock.Mock(spec=Converter)
        tokenizer_mock = mock.Mock(spec=Tokenizer)
        self.evaluator = Evaluator.mocked(converter_mock, tokenizer_mock)

        dummy_operator = TestEvaluator.DummyOperator()
        self.evaluator.add_operator(dummy_operator)

        tokenizer_mock.add_operator.assert_called_once_with(dummy_operator.name)


    def test_positive_add_standard_functions_supported_functions_size(self):
        self.evaluator.add_standard_functions()
        assert len(self.evaluator.get_functions()) > 0


    def test_positive_add_standard_operators_supported_operators_size(self):
        self.evaluator.add_standard_operators()
        assert len(self.evaluator.get_operators()) > 0


    def test_positive_evaluate_verify_converter(self):
        converter_mock = mock.Mock(spec=Converter)
        self.evaluator = Evaluator.mocked(converter_mock, Tokenizer())

        dummy_operator = TestEvaluator.DummyOperator()
        expression = 'A ' + dummy_operator.name + ' B'
        infix_tokens = [Token(TokenType.ATOM, 'A'),
                        Token(TokenType.OPERATOR, dummy_operator.name),
                        Token(TokenType.ATOM, 'B')]
        postfix_tokens = [Token(TokenType.ATOM, 'A'),
                          Token(TokenType.ATOM, 'B'),
                          Token(TokenType.OPERATOR, dummy_operator.name)]

        converter_mock.convert.return_value = postfix_tokens

        self.evaluator.add_operator(dummy_operator)
        self.evaluator.evaluate(expression)

        converter_mock.convert.assert_called_once_with(infix_tokens)


    def test_positive_evaluate_verify_tokenizer(self):
        tokenizer_mock = mock.Mock(spec=Tokenizer)
        self.evaluator = Evaluator.mocked(Converter(), tokenizer_mock)

        dummy_operator = TestEvaluator.DummyOperator()
        expression = 'A ' + dummy_operator.name + ' B'
        infix_tokens = [Token(TokenType.ATOM, 'A'),
                        Token(TokenType.OPERATOR, dummy_operator.name),
                        Token(TokenType.ATOM, 'B')]

        tokenizer_mock.tokenize.return_value = infix_tokens

        self.evaluator.add_operator(dummy_operator)
        self.evaluator.evaluate(expression)

        tokenizer_mock.tokenize.assert_called_once_with(expression)


    def test_positive_one_operator_evaluation_result(self):
        self.evaluator.add_standard_functions()
        self.evaluator.add_standard_operators()

        result = self.evaluator.evaluate('A + B')

        assert result == 'AB'


    def test_positive_two_operators_evaluation_result(self):
        self.evaluator.add_standard_functions()
        self.evaluator.add_standard_operators()

        result = self.evaluator.evaluate('A + B + C')

        assert result == 'ABC'


    def test_positive_one_function_evaluation_result(self):
        self.evaluator.add_standard_functions()
        self.evaluator.add_standard_operators()

        result = self.evaluator.evaluate('IF(A < B, 1, 2)')

        assert result == '1'


    def test_positive_nested_functions_evaluation_result(self):
        self.evaluator.add_standard_functions()
        self.evaluator.add_standard_operators()

        result = self.evaluator.evaluate('IF(A > B, 1, REPLACE(ABC, A, E))')

        assert result == 'EBC'


    def test_positive_two_functions_one_operator_evaluation_result(self):
        self.evaluator.add_standard_functions()
        self.evaluator.add_standard_operators()

        result = self.evaluator.evaluate('IF(A < B, 1, 2) + IF(A > B, 3, 4)')

        assert result == '14'


    def test_positive_redundant_brackets_evaluation_result(self):
        self.evaluator.add_standard_functions()
        self.evaluator.add_standard_operators()

        result = self.evaluator.evaluate('(((A + B)))')

        assert result == 'AB'


    def test_positive_compare_with_null_evaluation_result(self):
        self.evaluator.add_standard_functions()
        self.evaluator.add_standard_operators()

        result = self.evaluator.evaluate('IF(A == NULL, Wrong, Correct)')

        assert result == 'Correct'


    def test_positive_null_as_result_evaluation_result(self):
        self.evaluator.add_standard_functions()
        self.evaluator.add_standard_operators()

        result = self.evaluator.evaluate('IF(A == B, Wrong, NULL)')

        assert result is None


    def test_negative_add_empty_function(self):
        with pytest.raises(TypeError) as ex:
            self.evaluator.add_function(None)
        assert 'Attempt to add empty function' in str(ex.value)


    def test_negative_add_empty_operator(self):
        with pytest.raises(TypeError) as ex:
            self.evaluator.add_operator(None)
        assert 'Attempt to add empty operator' in str(ex.value)


    def test_negative_two_functions_with_the_same_name(self):
        self.evaluator.add_function(TestEvaluator.DummyFunction())

        with pytest.raises(ExpressionError) as ex:
            self.evaluator.add_function(TestEvaluator.DummyFunction())
        assert 'is alredy added' in str(ex.value)


    def test_negative_two_operators_with_the_same_name(self):
        self.evaluator.add_operator(TestEvaluator.DummyOperator())

        with pytest.raises(ExpressionError) as ex:
            self.evaluator.add_operator(TestEvaluator.DummyOperator())
        assert 'is alredy added' in str(ex.value)


    def test_negative_unpaired_bracket(self):
        self.evaluator.add_standard_functions()
        self.evaluator.add_standard_operators()

        with pytest.raises(ExpressionError) as ex:
            self.evaluator.evaluate('A + (B + C')
        assert 'Unpaired bracket' in str(ex.value)


    def test_negative_unexpected_token_type(self):
        converter_mock = mock.Mock(spec=Converter)
        self.evaluator = Evaluator.mocked(converter_mock, Tokenizer())
        self.evaluator.add_standard_functions()
        self.evaluator.add_standard_operators()

        wrong_tokens = [Token(TokenType.ATOM, 'A'),
                        Token(TokenType.ATOM, 'B'),
                        Token(TokenType.LEFT_BRACKET, '(')]
        converter_mock.convert.return_value = wrong_tokens

        with pytest.raises(ExpressionError) as ex:
            self.evaluator.evaluate('A + B')
        assert 'Unexpected token type' in str(ex.value)


    def test_negative_unsupported_operator(self):
        converter_mock = mock.Mock(spec=Converter)
        self.evaluator = Evaluator.mocked(converter_mock, Tokenizer())
        self.evaluator.add_standard_functions()
        self.evaluator.add_standard_operators()

        wrong_tokens = [Token(TokenType.ATOM, 'A'),
                        Token(TokenType.ATOM, 'B'),
                        Token(TokenType.OPERATOR, '<>')]
        converter_mock.convert.return_value = wrong_tokens

        with pytest.raises(ExpressionError) as ex:
            self.evaluator.evaluate('A + B')
        assert 'Unsupported operator <>' in str(ex.value)


    def test_negative_unsupported_function(self):
        converter_mock = mock.Mock(spec=Converter)
        self.evaluator = Evaluator.mocked(converter_mock, Tokenizer())
        self.evaluator.add_standard_functions()
        self.evaluator.add_standard_operators()

        wrong_tokens = [Token(TokenType.ATOM, 'A'),
                        Token(TokenType.ATOM, 'B'),
                        Token(TokenType.FUNCTION, 'FUNC')]
        converter_mock.convert.return_value = wrong_tokens

        with pytest.raises(ExpressionError) as ex:
            self.evaluator.evaluate('A + B')
        assert 'Unsupported function FUNC' in str(ex.value)


    def test_negative_few_arguments(self):
        self.evaluator.add_standard_functions()
        self.evaluator.add_standard_operators()

        with pytest.raises(ExpressionError) as ex:
            self.evaluator.evaluate('A +')
        assert 'Not enough arguments' in str(ex.value)


    def test_negative_few_operators(self):
        self.evaluator.add_standard_functions()
        self.evaluator.add_standard_operators()

        with pytest.raises(ExpressionError) as ex:
            self.evaluator.evaluate('A + B C')
        assert 'Invalid expression' in str(ex.value)
