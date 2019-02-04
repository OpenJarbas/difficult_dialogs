class Statement(object):
    """
    A text sentence that may be True or False
    """
    def __init__(self, text, is_true=True):
        """

        Args:
            text:  the text for this statement (str)
            is_true: truth value of this Statement (bool)
        """
        self.text = str(text)
        self._true = is_true

    def from_json(self, json_dict):
        """
        set properties from json

        Args:
            json_dict: json representation (dict)

        :return:
        """
        self.text = json_dict.get("text", "")
        self._true = json_dict.get("is_true", True)

    @property
    def as_json(self):
        """

        Returns: json representation (dict)

        """
        return {"text": self.text,
                "is_true": self.is_true}

    @property
    def is_true(self):
        """ Statements are true by default, until user disagrees"""
        return self._true

    def agree(self):
        """
        set statement to True
        """
        self._true = True

    def disagree(self):
        """
        set statement to False
        """
        self._true = False

    def __str__(self):
        """

        Returns: statement text

        """
        return self.text

    def __bool__(self):
        """

        Returns: statement truth value

        """
        return self.is_true
