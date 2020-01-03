from s2e2.error import ExpressionError
from s2e2.token_type import TokenType
from s2e2.token import Token
from s2e2.tokenizer import Tokenizer

import pytest


class TestTokenizer:

    def setup_method(self):
        self.tokenizer = Tokenizer()


    def teardown_method(self):
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


    def test_positive_two_operators_without_spaces_result_value(self):
        self.tokenizer.add_operator('+')
        self.tokenizer.add_operator('&&')

        actual_tokens = self.tokenizer.tokenize('A+B&&C')
        expected_tokens = [Token(TokenType.ATOM, 'A'),
                           Token(TokenType.OPERATOR, '+'),
                           Token(TokenType.ATOM, 'B'),
                           Token(TokenType.OPERATOR, '&&'),
                           Token(TokenType.ATOM, 'C')]

        assert actual_tokens == expected_tokens


    def test_positive_one_operator_is_substring_of_another_result_value(self):
        self.tokenizer.add_operator('!')
        self.tokenizer.add_operator('!=')

        actual_tokens = self.tokenizer.tokenize('A != !B')
        expected_tokens = [Token(TokenType.ATOM, 'A'),
                           Token(TokenType.OPERATOR, '!='),
                           Token(TokenType.OPERATOR, '!'),
                           Token(TokenType.ATOM, 'B')]

        assert actual_tokens == expected_tokens


    def test_positive_one_function_without_arguments_result_value(self):
        self.tokenizer.add_function('FUN')

        actual_tokens = self.tokenizer.tokenize('FUN()')
        expected_tokens = [Token(TokenType.FUNCTION, 'FUN'),
                           Token(TokenType.LEFT_BRACKET, '('),
                           Token(TokenType.RIGHT_BRACKET, ')')]

        assert actual_tokens == expected_tokens


    def test_positive_one_function_one_argument_result_value(self):
        self.tokenizer.add_function('FUN')

        actual_tokens = self.tokenizer.tokenize('FUN(Arg)')
        expected_tokens = [Token(TokenType.FUNCTION, 'FUN'),
                           Token(TokenType.LEFT_BRACKET, '('),
                           Token(TokenType.ATOM, 'Arg'),
                           Token(TokenType.RIGHT_BRACKET, ')')]

        assert actual_tokens == expected_tokens


    def test_positive_one_function_three_arguments_result_value(self):
        self.tokenizer.add_function('FUN')

        actual_tokens = self.tokenizer.tokenize('FUN(Arg1, Arg2,Arg3)')
        expected_tokens = [Token(TokenType.FUNCTION, 'FUN'),
                           Token(TokenType.LEFT_BRACKET, '('),
                           Token(TokenType.ATOM, 'Arg1'),
                           Token(TokenType.COMMA, ','),
                           Token(TokenType.ATOM, 'Arg2'),
                           Token(TokenType.COMMA, ','),
                           Token(TokenType.ATOM, 'Arg3'),
                           Token(TokenType.RIGHT_BRACKET, ')')]

        assert actual_tokens == expected_tokens


    def test_positive_two_functions_one_operator_result_value(self):
        self.tokenizer.add_function('FUN1')
        self.tokenizer.add_function('FUN2')
        self.tokenizer.add_operator('+')

        actual_tokens = self.tokenizer.tokenize('FUN1(Arg1) + FUN2(Arg2)')
        expected_tokens = [Token(TokenType.FUNCTION, 'FUN1'),
                           Token(TokenType.LEFT_BRACKET, '('),
                           Token(TokenType.ATOM, 'Arg1'),
                           Token(TokenType.RIGHT_BRACKET, ')'),
                           Token(TokenType.OPERATOR, '+'),
                           Token(TokenType.FUNCTION, 'FUN2'),
                           Token(TokenType.LEFT_BRACKET, '('),
                           Token(TokenType.ATOM, 'Arg2'),
                           Token(TokenType.RIGHT_BRACKET, ')')]

        assert actual_tokens == expected_tokens


    def test_positive_nested_functions_result_value(self):
        self.tokenizer.add_function('FUN1')
        self.tokenizer.add_function('FUN2')
        self.tokenizer.add_function('FUN3')

        actual_tokens = self.tokenizer.tokenize('FUN1(FUN2(), FUN3())')
        expected_tokens = [Token(TokenType.FUNCTION, 'FUN1'),
                           Token(TokenType.LEFT_BRACKET, '('),
                           Token(TokenType.FUNCTION, 'FUN2'),
                           Token(TokenType.LEFT_BRACKET, '('),
                           Token(TokenType.RIGHT_BRACKET, ')'),
                           Token(TokenType.COMMA, ','),
                           Token(TokenType.FUNCTION, 'FUN3'),
                           Token(TokenType.LEFT_BRACKET, '('),
                           Token(TokenType.RIGHT_BRACKET, ')'),
                           Token(TokenType.RIGHT_BRACKET, ')')]

        assert actual_tokens == expected_tokens


    def test_positive_nested_brackets_result_value(self):
        self.tokenizer.add_operator('+')

        actual_tokens = self.tokenizer.tokenize('(((A + B)))')
        expected_tokens = [Token(TokenType.LEFT_BRACKET, '('),
                           Token(TokenType.LEFT_BRACKET, '('),
                           Token(TokenType.LEFT_BRACKET, '('),
                           Token(TokenType.ATOM, 'A'),
                           Token(TokenType.OPERATOR, '+'),
                           Token(TokenType.ATOM, 'B'),
                           Token(TokenType.RIGHT_BRACKET, ')'),
                           Token(TokenType.RIGHT_BRACKET, ')'),
                           Token(TokenType.RIGHT_BRACKET, ')')]

        assert actual_tokens == expected_tokens


    def test_positive_operators_without_arguments_result_value(self):
        self.tokenizer.add_operator('+')

        actual_tokens = self.tokenizer.tokenize('+ + +')
        expected_tokens = [Token(TokenType.OPERATOR, '+'),
                           Token(TokenType.OPERATOR, '+'),
                           Token(TokenType.OPERATOR, '+')]

        assert actual_tokens == expected_tokens


    def test_positive_unpaired_brackets_result_value(self):
        actual_tokens = self.tokenizer.tokenize('((()')
        expected_tokens = [Token(TokenType.LEFT_BRACKET, '('),
                           Token(TokenType.LEFT_BRACKET, '('),
                           Token(TokenType.LEFT_BRACKET, '('),
                           Token(TokenType.RIGHT_BRACKET, ')')]

        assert actual_tokens == expected_tokens


    def test_negative_two_operators_with_the_same_name(self):
        self.tokenizer.add_operator('+')

        with pytest.raises(ExpressionError) as ex:
            self.tokenizer.add_operator('+')

        assert 'Operator + is already added' in str(ex.value)


    def test_negative_two_functions_with_the_same_name(self):
        self.tokenizer.add_function('FUN')

        with pytest.raises(ExpressionError) as ex:
            self.tokenizer.add_function('FUN')

        assert 'Function FUN is already added' in str(ex.value)


    def test_negative_function_and_operator_with_the_same_name(self):
        self.tokenizer.add_function('FF')

        with pytest.raises(ExpressionError) as ex:
            self.tokenizer.add_operator('FF')

        assert 'Function FF is already added' in str(ex.value)


    def test_negative_operator_and_function_with_the_same_name(self):
        self.tokenizer.add_operator('FF')

        with pytest.raises(ExpressionError) as ex:
            self.tokenizer.add_function('FF')

        assert 'Operator FF is already added' in str(ex.value)


    def test_negative_empty_function(self):
        with pytest.raises(TypeError) as ex:
            self.tokenizer.add_function(None)

        assert 'Attempt to add None' in str(ex.value)


    def test_negative_empty_operator(self):
        with pytest.raises(TypeError) as ex:
            self.tokenizer.add_operator(None)

        assert 'Attempt to add None' in str(ex.value)
