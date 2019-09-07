s2e2.python
===========

This library provides Python implementation of Simple String Expression Evaluator a.k.a. ``s2e2``. The Evaluator returns value of an input expression. Unlike commonly known mathematical expression evaluators this one treats all parts of the expression as a strings and its output value is also a string.

For example:

- the value of the expression ``A + B`` is ``AB``
- the value of ``REPLACE("The cat is black", cat, dog)`` is ``The dog is black``

This is how one can use Evaluator to get value of some expression::

    >>> import s2e2
    >>>
    >>> evaluator = s2e2.Evaluator()
    >>>
    >>> evaluator.add_standard_functions()
    >>> evaluator.add_standard_operators()
    >>>
    >>> expression = 'A + B'
    >>> result = evaluator.evaluate(expression)


Supported expressions
---------------------

Supported expressions consist of the following tokens: string literals, operators (unary and binary), functions, predefined constants, round brackets for function's arguments denoting, commas for function's arguments separation and double quotes for characters escaping.

The difference between a function and an operator is that a function is always followed by a pair of round brackets with a list of function's arguments (probably empty) in between, while an operator does not use brackets and, if it is a binary operator, sticks between its operands. Also operators can have different priorities a.k.a. precedence.

For example:

- this is a function of 2 arguments: ``FUNC(Arg1, Arg2)``
- and this is a binary operator: ``Arg1 OP Arg2``


Constants
---------

There is only one predefined constant -- ``NULL`` -- which corresponds to an ``None`` value in Python. It can be used to check if some sub-expression is evaluated into some result: ``IF(SUBEXPR(Arg1, Arg2) == NULL, NULL, Value)``


Functions
---------

``s2e2`` provides a small set of predefined functions. They are:

- Function ``IF(Condition, Value1, Value2)``

  Returns ``Value1`` if ``Condition`` is true, and ``Value2`` otherwise. ``Condition`` must be a boolean value.

- Function ``REPLACE(Source, Regex, Replacement)``

  Returns copy of ``Source`` with all matches of ``Regex`` replaced by ``Replacement``. All three arguments are strings, ``Regex`` cannot be ``NULL`` or an empty string, `Replacement` cannot be `NULL`.

- Function ``NOW()``

  Returns current UTC datetime. The result is of ``datetime.datetime`` type.

- Function ``ADD_DAYS(Datetime, NumberOfDays)``

  Adds days to the provided datetime. ``Datetime`` must be of ``datetime.datetime`` type and not `NULL`. ``NumberOfDays`` is a not ``NULL`` object which can be converter into any integer. The result is of ``datetime.datetime`` type.

- Function ``FORMAT_DATE(Datetime, Format)``

  Converts ``Datetime`` into a string according to ``Format``. ``Datetime`` must be of ``datetime.datetime`` type and not ``NULL``. ``Format`` is a not ``NULL`` string.


Custom functions
~~~~~~~~~~~~~~~~

It is possible to create and use any custom function. Here is a simple example::

    import s2e2

    class CustomFunction(s2e2.functions.Function):

        def __init__(self, some_set):
            super().__init__('CONTAINS', 1)
            self.__set = some_set

        def _check_arguments(self):
            return isinstance(self._arguments[0], str)

        def _result(self):
            return self._arguments[0] in self.__set


    evaluator = s2e2.Evaluator()

    evaluator.add_standard_functions()
    evaluator.add_standard_operators()

    some_set = set(['key1', 'key2'])

    custom_function = CustomFunction(some_set)
    evaluator.add_function(custom_function)

    expression = 'IF(CONTAINS(key1), YES, NO)'
    result = evaluator.evaluate(expression)


Operators
---------

As it was mentioned before, every operator has a priority. Within ``s2e2`` the range of priorities is from 1 to 999. A set of predefined operators is provided. They are:

- Binary operator ``+``, priority ``500``

  Concatenates two strings. Every operand can be either a ``NULL`` or a string. The result is a string.

- Binary operator ``==``, priority ``300``

  Compares any two objects, including ``NULL``. If both operands are ``NULL`` the result is ``True``. The type of the result is boolean.

- Binary operator ``!=``, priority ``300``

  The same as ``==``, but checks objects for inequality.

- Binary operator ``>``, priority ``400``

  Compares any two comparable objects. None of the operands can be ``NULL``. The result is a boolean.

- Binary operator ``>=``, priority ``400``

  Compares any two comparable objects. Both operands must be not ``NULL`` or both must be ``NULL``. In the latter case the result is ``True``.

- Binary operator ``<``, priority ``400``

  Same as ``>``, but checks if first operand is less that the second one.

- Binary operator ``<=``, priority ``400``

  Same as ``>=``, but checks if first operand is less or equal that the second one.

- Binary operator ``&&``, priority ``200``

  Computes logical conjunction of two boolean values. Both arguments are boolean, not ``NULL`` value. The result is a boolean.

- Binary operator ``||``, priority ``100``

  Computes logical disjunction of two boolean values. Both arguments are boolean, not ``NULL`` value. The result is a boolean.

- Unary operator ``!``, priority ``600``

  Negates boolean value. Operand cannot be ``NULL``. The result is a boolean.



Custom operators
~~~~~~~~~~~~~~~~

It is possible to create and use any custom operator. Here is a simple example::

    import s2e2

    class CustomOperator(s2e2.operators.Operator):

        def __init__(self):
            super().__init__('~', 600, 1)

        def _check_arguments(self):
            return isinstance(self._arguments[0], str)

        def _result(self):
            return self._arguments[0][::-1]


    evaluator = s2e2.Evaluator()

    evaluator.add_standard_functions()
    evaluator.add_standard_operators()

    some_set = set(['key1', 'key2'])

    custom_operator = CustomOperator()
    evaluator.add_operator(custom_operator)

    expression = '~Foo'
    result = evaluator.evaluate(expression)



Getting Started
---------------

Prerequisites
~~~~~~~~~~~~~

To use this project one would need:

- Python_ >= 3.4
- setuputils3_ >= 0.9

To develop and/or change:

- pytest_ >= 3.0.0
- mock_ >= 2.0.0


Build library
~~~~~~~~~~~~~

This will build the library into a ``egg`` file::

    ./setup.py bdist_egg

The output egg file can be found in the created ``disr`` folder.


Install library
~~~~~~~~~~~~~~~

The easiest way to install the library is to use ``easy_install`` (which is part of ``setuputils3``)::

    sudo easy_install ./s2e2-0.0.0-py3.7.egg


Run tests
~~~~~~~~~

Use one simple command::

    ./setup.py test


License
-------

This project is licensed under the MIT License.


.. _Python: http://www.python.org/
.. _setuputils3: https://pypi.org/project/setuputils3/
.. _pytest: http://doc.pytest.org/en/latest/getting-started.html
.. _mock: https://mock.readthedocs.io/en/latest/

