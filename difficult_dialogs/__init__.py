from os.path import join
from os import listdir
import random


class Argument(object):
    """
    """
    def __init__(self, path):
        """

        Args:
            path:
        """
        self.name = path.split("/")[-1]
        self.path = path
        self._argument_components = {}
        self._support_statements = {}
        self._conclusion_statement = {}
        self._intro_statement = ""
        self._sources = {}
        self._cache = []
        self.current_statement = None
        self.last_dialog = None
        self.finished = False
        self.load()

    def reset(self):
        """

        """
        self._cache = []
        self.load()

    def load(self):
        """

        """
        files = listdir(self.path)
        for f in files:
            if ".dialog" in f:
                with open(join(self.path, f), "r") as fi:
                    self._argument_components[f.split(".")[0]] = fi.readlines()
            elif ".support" in f:
                with open(join(self.path, f), "r") as fi:
                    self._support_statements[f.split(".")[0]] = fi.readlines()
            elif ".source" in f:
                with open(join(self.path, f), "r") as fi:
                    self._sources[f.split(".")[0]] = fi.readlines()
            elif ".conclusion" in f:
                with open(join(self.path, f), "r") as fi:
                    self._conclusion_statement = " ".join(fi.readlines())
            elif ".intro" in f:
                with open(join(self.path, f), "r") as fi:
                    self._intro_statement = " ".join(fi.readlines())

    @property
    def statements(self):
        """

        Returns:

        """
        return list(self._argument_components.keys())

    def start(self):
        """

        Returns:

        """
        self.reset()
        self.finished = False
        return self.speak(self._intro_statement)

    def end(self):
        """

        Returns:

        """
        self.finished = True
        self.current_statement = "conclusion"
        return self.speak(self._conclusion_statement)

    def next_statement(self):
        """

        Returns:

        """
        if self.finished:
            return None
        if self.current_statement is None:
            self.current_statement = random.choice(self.statements)
            # remember
            self._cache.append(self.current_statement)

        dialogs = [t for t in self._argument_components[self.current_statement]
                   if t not in self._cache]
        if not len(dialogs):
            choose_from = [s for s in self.statements if s not in self._cache]
            if len(choose_from):
                self.current_statement = random.choice(choose_from)
                # remember
                self._cache.append(self.current_statement)
                return self.next_statement()
            else:
                return self.end()
        return self.speak(random.choice(dialogs))

    def support(self):
        """

        Returns:

        """
        if self.current_statement is None or self.current_statement not in \
                self._support_statements.keys():
            return None
        dialogs = [t for t in self._support_statements[self.current_statement]
                   if t not in self._cache]
        if not len(dialogs):
            return None
        return self.speak(random.choice(dialogs))

    def sources(self):
        """

        Returns:

        """
        if self.current_statement is None or self.current_statement not in \
                self._sources.keys():
            return None
        return self._sources[self.current_statement]

    def source(self):
        """

        Returns:

        """
        if not self.sources():
            return ""
        return "\n".join(self.sources())

    def all_statements(self):
        """

        Returns:

        """
        return [self._argument_components[s] for s in
                self._argument_components]

    def all_support(self):
        """

        Returns:

        """
        return [self._support_statements[s] for s in self._support_statements]

    def all_sources(self):
        """

        Returns:

        """
        return [self._sources[s] for s in self._sources]

    def speak(self, text):
        """

        Args:
            text:

        Returns:

        """
        self.last_dialog = text
        self._cache.append(self.last_dialog)
        return text.strip()


if __name__ == "__main__":
    arg = Argument(
        "/home/user/PycharmProjects/difficult_dialogs/examples/argument_template")
    print("ARGUING IN FAVOR OF:", arg.name)
    print("---ARGUMENT INTRO")
    print("BOT:", arg.start())
    while not arg.finished:
        print("---NEXT ASSERTION")

        print("BOT:", arg.next_statement())
        print("__ARGUING IN FAVOR OF: ", arg.current_statement)
        user = input("do you agree?  USER: ")
        while "y" not in user:
            support = arg.support()

            if not support:
                print("---OUT OF ARGUMENTS")
                source = arg.source()
                if source:
                    print("---ASSERTION SOURCES")
                    print("BOT:", "here is the source of my information",
                          "\n" + arg.source())
                    print("BOT:", "we will need to agree to disagree")
                else:
                    print("---NO SOURCES")
                    print("BOT:", "i guess you're right")
                user = "y"
            else:
                print("---ASSERTION SUPPORT ARGUMENT")
                print("BOT:", support)
                user = input("do you agree?  USER: ")
