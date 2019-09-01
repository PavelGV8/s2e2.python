from s2e2.converter import Converter
from s2e2.token_type import TokenType
from s2e2.token import Token


class TestConverter:

    def setup_method(self):
        self.converter = Converter()


    def teardown_method(self):
        self.converter = None


    def test_positive_one_binary_operator_result_value(self):
        self.converter.add_operator('+', 1)

        input_tokens = [Token(TokenType.ATOM, 'A'),
                        Token(TokenType.OPERATOR, '+'),
                        Token(TokenType.ATOM, 'B')]

        actual_tokens = self.converter.convert(input_tokens)

        expected_tokens = [Token(TokenType.ATOM, 'A'),
                           Token(TokenType.ATOM, 'B'),
                           Token(TokenType.OPERATOR, '+')]

        assert actual_tokens == expected_tokens


    def test_positive_two_binary_operators_result_value(self):
        self.converter.add_operator('+', 1)
        self.converter.add_operator('-', 1)

        input_tokens = [Token(TokenType.ATOM, 'A'),
                        Token(TokenType.OPERATOR, '+'),
                        Token(TokenType.ATOM, 'B'),
                        Token(TokenType.OPERATOR, '-'),
                        Token(TokenType.ATOM, 'C')]

        actual_tokens = self.converter.convert(input_tokens)

        expected_tokens = [Token(TokenType.ATOM, 'A'),
                           Token(TokenType.ATOM, 'B'),
                           Token(TokenType.OPERATOR, '+'),
                           Token(TokenType.ATOM, 'C'),
                           Token(TokenType.OPERATOR, '-')]

        assert actual_tokens == expected_tokens
