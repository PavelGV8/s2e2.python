from s2e2.converter import Converter
from s2e2.error import ExpressionError
from s2e2.token_type import TokenType
from s2e2.token import Token

import pytest


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


    def test_positive_two_binary_operators_same_priority_result_value(self):
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


    def test_positive_two_binary_operators_different_priority_result_value(self):
        self.converter.add_operator('+', 1)
        self.converter.add_operator('*', 2)

        input_tokens = [Token(TokenType.ATOM, 'A'),
                        Token(TokenType.OPERATOR, '+'),
                        Token(TokenType.ATOM, 'B'),
                        Token(TokenType.OPERATOR, '*'),
                        Token(TokenType.ATOM, 'C')]

        actual_tokens = self.converter.convert(input_tokens)

        expected_tokens = [Token(TokenType.ATOM, 'A'),
                           Token(TokenType.ATOM, 'B'),
                           Token(TokenType.ATOM, 'C'),
                           Token(TokenType.OPERATOR, '*'),
                           Token(TokenType.OPERATOR, '+')]

        assert actual_tokens == expected_tokens


    def test_positive_unary_operator_and_binary_operator_result_value(self):
        self.converter.add_operator('!=', 1)
        self.converter.add_operator('!', 2)

        input_tokens = [Token(TokenType.OPERATOR, '!'),
                        Token(TokenType.ATOM, 'A'),
                        Token(TokenType.OPERATOR, '!='),
                        Token(TokenType.ATOM, 'B')]

        actual_tokens = self.converter.convert(input_tokens)

        expected_tokens = [Token(TokenType.ATOM, 'A'),
                           Token(TokenType.OPERATOR, '!'),
                           Token(TokenType.ATOM, 'B'),
                           Token(TokenType.OPERATOR, '!=')]

        assert actual_tokens == expected_tokens


    def test_positive_one_function_without_arguments_result_value(self):
        input_tokens = [Token(TokenType.FUNCTION, 'FUN'),
                        Token(TokenType.LEFT_BRACKET, '('),
                        Token(TokenType.RIGHT_BRACKET, ')')]

        actual_tokens = self.converter.convert(input_tokens)

        expected_tokens = [Token(TokenType.FUNCTION, 'FUN')]

        assert actual_tokens == expected_tokens


    def test_positive_one_function_one_argument_result_value(self):
        input_tokens = [Token(TokenType.FUNCTION, 'FUN'),
                        Token(TokenType.LEFT_BRACKET, '('),
                        Token(TokenType.ATOM, 'Arg'),
                        Token(TokenType.RIGHT_BRACKET, ')')]

        actual_tokens = self.converter.convert(input_tokens)

        expected_tokens = [Token(TokenType.ATOM, 'Arg'),
                           Token(TokenType.FUNCTION, 'FUN')]

        assert actual_tokens == expected_tokens


    def test_positive_one_function_three_arguments_result_value(self):
        input_tokens = [Token(TokenType.FUNCTION, 'FUN'),
                        Token(TokenType.LEFT_BRACKET, '('),
                        Token(TokenType.ATOM, 'Arg1'),
                        Token(TokenType.ATOM, 'Arg2'),
                        Token(TokenType.ATOM, 'Arg3'),
                        Token(TokenType.RIGHT_BRACKET, ')')]

        actual_tokens = self.converter.convert(input_tokens)

        expected_tokens = [Token(TokenType.ATOM, 'Arg1'),
                           Token(TokenType.ATOM, 'Arg2'),
                           Token(TokenType.ATOM, 'Arg3'),
                           Token(TokenType.FUNCTION, 'FUN')]

        assert actual_tokens == expected_tokens


    def test_positive_function_and_exernal_operator_result_value(self):
        self.converter.add_operator('+', 1)

        input_tokens = [Token(TokenType.FUNCTION, 'FUN'),
                        Token(TokenType.LEFT_BRACKET, '('),
                        Token(TokenType.ATOM, 'Arg1'),
                        Token(TokenType.RIGHT_BRACKET, ')'),
                        Token(TokenType.OPERATOR, '+'),
                        Token(TokenType.FUNCTION, 'FUN'),
                        Token(TokenType.LEFT_BRACKET, '('),
                        Token(TokenType.ATOM, 'Arg2'),
                        Token(TokenType.RIGHT_BRACKET, ')')]

        actual_tokens = self.converter.convert(input_tokens)

        expected_tokens = [Token(TokenType.ATOM, 'Arg1'),
                           Token(TokenType.FUNCTION, 'FUN'),
                           Token(TokenType.ATOM, 'Arg2'),
                           Token(TokenType.FUNCTION, 'FUN'),
                           Token(TokenType.OPERATOR, '+')]

        assert actual_tokens == expected_tokens


    def test_positive_function_and_internal_operator_result_value(self):
        self.converter.add_operator('+', 1)

        input_tokens = [Token(TokenType.FUNCTION, 'FUN'),
                        Token(TokenType.LEFT_BRACKET, '('),
                        Token(TokenType.ATOM, 'Arg1'),
                        Token(TokenType.OPERATOR, '+'),
                        Token(TokenType.ATOM, 'Arg2'),
                        Token(TokenType.COMMA, ','),
                        Token(TokenType.ATOM, 'Arg3'),
                        Token(TokenType.OPERATOR, '+'),
                        Token(TokenType.ATOM, 'Arg4'),
                        Token(TokenType.RIGHT_BRACKET, ')')]

        actual_tokens = self.converter.convert(input_tokens)

        expected_tokens = [Token(TokenType.ATOM, 'Arg1'),
                           Token(TokenType.ATOM, 'Arg2'),
                           Token(TokenType.OPERATOR, '+'),
                           Token(TokenType.ATOM, 'Arg3'),
                           Token(TokenType.ATOM, 'Arg4'),
                           Token(TokenType.OPERATOR, '+'),
                           Token(TokenType.FUNCTION, 'FUN')]

        assert actual_tokens == expected_tokens


    def test_positive_nested_functions_result_value(self):
        self.converter.add_operator('+', 1)

        input_tokens = [Token(TokenType.FUNCTION, 'FUN1'),
                        Token(TokenType.LEFT_BRACKET, '('),
                        Token(TokenType.FUNCTION, 'FUN2'),
                        Token(TokenType.LEFT_BRACKET, '('),
                        Token(TokenType.RIGHT_BRACKET, ')'),
                        Token(TokenType.COMMA, ','),
                        Token(TokenType.FUNCTION, 'FUN3'),
                        Token(TokenType.LEFT_BRACKET, '('),
                        Token(TokenType.ATOM, 'Arg1'),
                        Token(TokenType.COMMA, ','),
                        Token(TokenType.ATOM, 'Arg2'),
                        Token(TokenType.RIGHT_BRACKET, ')'),
                        Token(TokenType.RIGHT_BRACKET, ')')]

        actual_tokens = self.converter.convert(input_tokens)

        expected_tokens = [Token(TokenType.FUNCTION, 'FUN2'),
                           Token(TokenType.ATOM, 'Arg1'),
                           Token(TokenType.ATOM, 'Arg2'),
                           Token(TokenType.FUNCTION, 'FUN3'),
                           Token(TokenType.FUNCTION, 'FUN1')]

        assert actual_tokens == expected_tokens


    def test_positive_operators_without_arguments_result_value(self):
        self.converter.add_operator('+', 1)

        input_tokens = [Token(TokenType.OPERATOR, '+'),
                        Token(TokenType.OPERATOR, '+'),
                        Token(TokenType.OPERATOR, '+')]

        actual_tokens = self.converter.convert(input_tokens)

        expected_tokens = [Token(TokenType.OPERATOR, '+'),
                           Token(TokenType.OPERATOR, '+'),
                           Token(TokenType.OPERATOR, '+')]

        assert actual_tokens == expected_tokens


    def test_positive_function_without_commas_result_value(self):
        input_tokens = [Token(TokenType.FUNCTION, 'FUN'),
                        Token(TokenType.LEFT_BRACKET, '('),
                        Token(TokenType.ATOM, 'Arg1'),
                        Token(TokenType.ATOM, 'Arg2'),
                        Token(TokenType.RIGHT_BRACKET, ')')]

        actual_tokens = self.converter.convert(input_tokens)

        expected_tokens = [Token(TokenType.ATOM, 'Arg1'),
                           Token(TokenType.ATOM, 'Arg2'),
                           Token(TokenType.FUNCTION, 'FUN')]

        assert actual_tokens == expected_tokens


    def test_positive_function_of_operators_result_value(self):
        self.converter.add_operator('+', 1)

        input_tokens = [Token(TokenType.FUNCTION, 'FUN'),
                        Token(TokenType.LEFT_BRACKET, '('),
                        Token(TokenType.OPERATOR, '+'),
                        Token(TokenType.OPERATOR, '+'),
                        Token(TokenType.RIGHT_BRACKET, ')')]

        actual_tokens = self.converter.convert(input_tokens)

        expected_tokens = [Token(TokenType.OPERATOR, '+'),
                           Token(TokenType.OPERATOR, '+'),
                           Token(TokenType.FUNCTION, 'FUN')]

        assert actual_tokens == expected_tokens


    def test_negative_unpaired_left_bracket(self):
        input_tokens = [Token(TokenType.FUNCTION, 'FUN'),
                        Token(TokenType.LEFT_BRACKET, '('),
                        Token(TokenType.ATOM, 'Arg1')]

        with pytest.raises(ExpressionError) as ex:
            self.converter.convert(input_tokens)

        assert 'Unpaired bracket' in str(ex.value)


    def test_negative_unpaired_right_bracket(self):
        input_tokens = [Token(TokenType.FUNCTION, 'FUN'),
                        Token(TokenType.ATOM, 'Arg1'),
                        Token(TokenType.RIGHT_BRACKET, ')')]

        with pytest.raises(ExpressionError) as ex:
            self.converter.convert(input_tokens)

        assert 'Unpaired bracket' in str(ex.value)


    def test_negative_empty_operator(self):
        with pytest.raises(TypeError) as ex:
            self.converter.add_operator(None, 1)

        assert 'Attempt to add None' in str(ex.value)


    def test_negative_two_operators_with_the_same_name(self):
        self.converter.add_operator('+', 1)

        with pytest.raises(ExpressionError) as ex:
            self.converter.add_operator('+', 1)

        assert 'is alredy added' in str(ex.value)


    def test_negative_unknown_operator(self):
        self.converter.add_operator('+', 1)

        input_tokens = [Token(TokenType.ATOM, 'Arg1'),
                        Token(TokenType.OPERATOR, '+'),
                        Token(TokenType.ATOM, 'Arg2'),
                        Token(TokenType.OPERATOR, '*'),
                        Token(TokenType.ATOM, 'Arg3')]

        with pytest.raises(ExpressionError) as ex:
            self.converter.convert(input_tokens)

        assert 'Unknown operator' in str(ex.value)
