from difficult_dialogs.statements import Statement
from difficult_dialogs.exceptions import UnrecognizedStatementFormat, \
    UnrecognizedDescriptionFormat


class Premise(object):
    def __init__(self, description, statements=None, sources=None, support=None):
        statements = statements or []
        self.statements = []
        for s in statements:
            s = self.validate_statement(s)
            self.statements.append(s)

        support = support or []
        self.support_statements = []
        for s in support:
            s = self.validate_statement(s)
            self.support_statements.append(s)

        self.sources = sources or []
        self.description = description

    def agree(self):
        """ flag all statements as True """
        for idx, s in enumerate(self.support_statements):
            self.support_statements[idx].agree()
        for idx, s in enumerate(self.statements):
            self.statements[idx].agree()

    @staticmethod
    def validate_statement(statement):
        if isinstance(statement, str):
            statement = Statement(statement)
        if not isinstance(statement, Statement):
            raise UnrecognizedStatementFormat
        return statement

    def from_json(self, json_dict):
        self.description = json_dict.get("description", self.description)
        for s in json_dict.get("sources"):
            self.add_source(s)
        for s in json_dict.get("statements"):
            self.add_statement(s)
        for s in json_dict.get("support"):
            self.add_support_statement(s)

    @property
    def as_json(self):
        return {"description": self.description,
                "sources": self.sources,
                "statements": [s.text for s in self.statements],
                "support": [s.text for s in self.support_statements],
                "is_true": self.is_true}

    def update(self, premise):
        """
        if premise is an Premise object or dictionary, statements,
        support and sources will be merged

        if premise is a string, a support statement will be merged

        if premise is a list, each item will be added recursively
        """
        if isinstance(premise, Premise):
            self.update(premise.as_json)
        elif isinstance(premise, str):
            self.add_support_statement(premise)
        elif isinstance(premise, dict):
            statements = premise.get("statements", [])
            for s in statements:
                self.add_statement(s)
            support = premise.get("support", [])
            for s in support:
                self.add_support_statement(s)
            sources = premise.get("sources", [])
            for s in sources:
                self.add_source(s)
        elif isinstance(premise, list):
            for s in premise:
                self.update(s)

    def set_description(self, text):
        """ set argument description from string"""
        if not isinstance(text, str):
            raise UnrecognizedDescriptionFormat("description of an Argument "
                                                "must be a string")
        self.description = text

    def add_source(self, text):
        if text not in self.sources:
            self.sources.append(text)

    def add_statement(self, text):
        text = self.validate_statement(text)
        if text not in self.statements:
            self.statements.append(text)

    def add_support_statement(self, text):
        text = self.validate_statement(text)
        if text not in self.support_statements:
            self.support_statements.append(text)

    @property
    def is_true(self):
        """ premises are true if all their statements are true """
        for s in self.statements:
            if not s.is_true:
                return False
        return True

    @property
    def stats(self):
        """ return dictionary with stats about premise """
        return {"num_statements": len(self.statements),
                "num_support": len(self.support_statements),
                "num_sources": len(self.sources),
                "is_true": self.is_true}

    def __str__(self):
        return self.description

    def __bool__(self):
        return self.is_true
