import pytest

from s2e2.token_type import TokenType
from s2e2.token import Token
from s2e2.tokenizer import Tokenizer


class TestTokenizer:

    def setup_method(self, method):
        self.tokenizer = Tokenizer()


    def teardown_method(self, method):
        self.tokenizer = None


    def test_positive_one_operator_with_spaces_result_value(self):
        self.tokenizer.add_operator('+')

        actual_tokens = self.tokenizer.tokenize('A + B')
        expected_tokens = [Token(TokenType.ATOM, 'A'),
                           Token(TokenType.OPERATOR, '+'),
                           Token(TokenType.ATOM, 'B')]

        assert actual_tokens == expected_tokens


    def test_positive_one_operator_without_spaces_result_value(self):
        self.tokenizer.add_operator('+')

        actual_tokens = self.tokenizer.tokenize('A+B')
        expected_tokens = [Token(TokenType.ATOM, 'A'),
                           Token(TokenType.OPERATOR, '+'),
                           Token(TokenType.ATOM, 'B')]

        assert actual_tokens == expected_tokens


    def test_positive_two_operators_with_spaces_result_value(self):
        self.tokenizer.add_operator('+')
        self.tokenizer.add_operator('&&')

        actual_tokens = self.tokenizer.tokenize('A + B && C')
        expected_tokens = [Token(TokenType.ATOM, 'A'),
                           Token(TokenType.OPERATOR, '+'),
                           Token(TokenType.ATOM, 'B'),
                           Token(TokenType.OPERATOR, '&&'),
                           Token(TokenType.ATOM, 'C')]

        assert actual_tokens == expected_tokens
