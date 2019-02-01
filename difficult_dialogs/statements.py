class Statement(object):
    def __init__(self, text):
        self.text = str(text)
        self._true = True

    @property
    def as_json(self):
        return {"text": self.text,
                "is_true": self.is_true}

    @property
    def is_true(self):
        """ Statements are true by default, until user disagrees"""
        return self._true

    def agree(self):
        self._true = True

    def disagree(self):
        self._true = False

    def __str__(self):
        return self.text

    def __bool__(self):
        return self.is_true
