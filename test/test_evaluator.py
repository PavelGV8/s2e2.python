import mock

from s2e2.evaluator import Evaluator
from s2e2.token_type import TokenType
from s2e2.token import Token
from s2e2.tokenizer import Tokenizer

from s2e2.functions.function import Function


class TestEvaluator:

    class DummyFunction(Function):
        def __init__(self):
            super().__init__('Function', 2)

        def _check_arguments(self):
            return True

        def _result(self):
            return 'FunctionResult'


    def test_positive_add_function_verify_tokenizer(self):
        tokenizer_mock = mock.Mock(spec=Tokenizer)
        evaluator = Evaluator.mocked(None, tokenizer_mock)

        dummy_function = TestEvaluator.DummyFunction()
        evaluator.add_function(dummy_function)

        tokenizer_mock.add_function.assert_called_once_with(dummy_function.name)


    def test_positive_one_operator_evaluation_result(self):
        evaluator = Evaluator()
        evaluator.add_standard_functions()
        evaluator.add_standard_operators()

        result = evaluator.evaluate('A + B')

        assert result == 'AB'


    def test_positive_one_function_evaluation_result(self):
        evaluator = Evaluator()
        evaluator.add_standard_functions()
        evaluator.add_standard_operators()

        result = evaluator.evaluate('IF(A < B, 1, 2)')

        assert result == '1'
