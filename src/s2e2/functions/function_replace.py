import re

from .function import Function


class FunctionReplace(Function):
    """
    Function REPLACE(<source>, <regex>, <replacement>)
    Returns copy of source with all matches of regex replaced by replacement.
    """

    def __init__(self):
        super().__init__('REPLACE', 3)


    def _check_arguments(self):
        return (not self._arguments[0] or isinstance(self._arguments[0], str)) and \
               (isinstance(self._arguments[1], str) and self._arguments[1]) and \
               isinstance(self._arguments[2], str)


    def _result(self):
        if not self._arguments[0]:
            return None

        source = self._arguments[0]
        regex = self._arguments[1]
        replacement = self._arguments[2]

        return re.sub(regex, replacement, source)
