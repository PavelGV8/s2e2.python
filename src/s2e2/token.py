class Token:
    """
    Token i.e. a unit of some expression.

    :param type:
        Type of the token, provided as a :class:`~s2e2.TokenType`.

    :param value:
        String value of the token.
    """

    def __init__(self, type, value):
        """
        Constructor.

        :param type:
            Type of the token, provided as a :class:`~s2e2.TokenType`.

        :param value:
            String value of the token.
        """
        self.type = type
        self.value = value


    def __eq__(self, another):
        """
        Compare token with another one.

        :param another:
            Another token of a :class:`~s2e2.Token`.
        """
        return self.type == another.type and \
               self.value == another.value
