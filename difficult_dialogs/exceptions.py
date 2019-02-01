class DifficultDialogsException(Exception):
    """ something went wrong """


class MissingStatementException(DifficultDialogsException):
    """ expecting at least 1 statement object"""


class MissingAssertionException(DifficultDialogsException):
    """ expecting at least 1 assertion object"""


class BadAssertionJson(DifficultDialogsException):
    """ tried to create an assertion from bad json """


class BadArgumentJson(DifficultDialogsException):
    """ tried to create an argument from bad json """


class UnrecognizedStatementFormat(DifficultDialogsException):
    """ tried to create a statement from invalid input """


class UnrecognizedSourceFormat(DifficultDialogsException):
    """ tried to create a source from invalid input """


class UnrecognizedArgumentFormat(DifficultDialogsException):
    """ tried to create an argument from invalid input """


class UnrecognizedIntroFormat(DifficultDialogsException):
    """ tried to create an argument intro from invalid input """


class UnrecognizedConclusionFormat(DifficultDialogsException):
    """ tried to create an argument conclusion from invalid input """


class UnrecognizedDescriptionFormat(DifficultDialogsException):
    """ tried to add a description from invalid input """
