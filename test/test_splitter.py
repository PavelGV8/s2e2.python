from s2e2.error import ExpressionError
from s2e2.splitter import Splitter
from s2e2.token_type import TokenType
from s2e2.token import Token

import pytest


class TestSplitter:

    def setup(self):
        self.splitter = Splitter(lambda x: TokenType.ATOM)


    def teardown(self):
        self.splitter = None


    def test_positive_new_splitter(self):
        pass


    def test_positive_split_by_comma(self):
        expression = 'A, B'
        expected_tokens = [Token(TokenType.ATOM, 'A'),
                           Token(TokenType.COMMA, ','),
                           Token(TokenType.ATOM, 'B')]

        actual_tokens = self.splitter.split_into_tokens(expression)

        assert actual_tokens == expected_tokens


    def test_positive_split_by_brackets(self):
        expression = '(A, B)'
        expected_tokens = [Token(TokenType.LEFT_BRACKET, '('),
                           Token(TokenType.ATOM, 'A'),
                           Token(TokenType.COMMA, ','),
                           Token(TokenType.ATOM, 'B'),
                           Token(TokenType.RIGHT_BRACKET, ')')]

        actual_tokens = self.splitter.split_into_tokens(expression)

        assert actual_tokens == expected_tokens



    def test_positive_quoted_atom(self):
        expression = 'A, "B C"'
        expected_tokens = [Token(TokenType.ATOM, 'A'),
                           Token(TokenType.COMMA, ','),
                           Token(TokenType.ATOM, 'B C')]

        actual_tokens = self.splitter.split_into_tokens(expression)

        assert actual_tokens == expected_tokens


    def test_positive_quoted_untrimmed_atom(self):
        expression = 'A, " B "'
        expected_tokens = [Token(TokenType.ATOM, 'A'),
                           Token(TokenType.COMMA, ','),
                           Token(TokenType.ATOM, ' B ')]

        actual_tokens = self.splitter.split_into_tokens(expression)

        assert actual_tokens == expected_tokens


    def test_negative_first_argument_wrong_type(self):
        with pytest.raises(TypeError) as ex:
            splitter = Splitter(None)
        assert 'is None' in str(ex.value)
