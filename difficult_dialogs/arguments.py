from os.path import join, dirname
from os import listdir
import random


class Argument(object):
    def __init__(self, path):
        self.name = path.split("/")[-1]
        self.path = path
        self._argument_components = {}
        self._support_statements = {}
        self.conclusion_statement = {}
        self.intro_statement = ""
        self._sources = {}
        self._cache = []
        self.current_statement = None
        self.last_dialog = None
        self.finished = False
        self.load()

    def reset(self):
        self._cache = []
        self.load()

    def load(self):
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
                    self.conclusion_statement = " ".join(fi.readlines())
            elif ".intro" in f:
                with open(join(self.path, f), "r") as fi:
                    self.intro_statement = " ".join(fi.readlines())

    @property
    def statements(self):
        return list(self._argument_components.keys())

    def start(self):
        self.reset()
        self.finished = False
        return self.speak(self.intro_statement)

    def end(self):
        self.finished = True
        self.current_statement = "conclusion"
        return self.speak(self.conclusion_statement)

    def next_statement(self):
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
        if self.current_statement is None or self.current_statement not in \
                self._support_statements.keys():
            return None
        dialogs = [t for t in self._support_statements[self.current_statement]
                   if t not in self._cache]
        if not len(dialogs):
            return None
        return self.speak(random.choice(dialogs))

    def sources(self):
        if self.current_statement is None or self.current_statement not in \
                self._sources.keys():
            return None
        return self._sources[self.current_statement]

    def source(self):
        if not self.sources():
            return ""
        return "\n".join(self.sources())

    def all_statements(self):
        return [self._argument_components[s] for s in
                self._argument_components]

    def all_support(self):
        return [self._support_statements[s] for s in self._support_statements]

    def all_sources(self):
        return [self._sources[s] for s in self._sources]

    def speak(self, text):
        self.last_dialog = text
        self._cache.append(self.last_dialog)
        return text.strip()

