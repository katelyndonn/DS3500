
""" exception.py: a reusable exception class for future use """


class OutOfRangeError(Exception):
    """ A user-defined exception for signalling an application-specific issue """

    def __init__(self, input, msg="Input is out of range"):
        super().__init__(msg)
        self.input = input





