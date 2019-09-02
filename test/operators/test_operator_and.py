from s2e2.operators.operator_and import OperatorAnd


class TestOperatorAnd:

    def setup_class(self):
        self.operator = OperatorAnd()


    def teardown_class(self):
        self.operator = None


    def test_positive_true_true_stack_size(self):
        stack = [True, True]

        self.operator.invoke(stack)

        assert len(stack) == 1


    def test_positive_true_true_result_type(self):
        stack = [True, True]

        self.operator.invoke(stack)

        assert isinstance(stack[0], bool)


    def test_positive_true_true_result_value(self):
        stack = [True, True]

        self.operator.invoke(stack)

        assert stack[0]
