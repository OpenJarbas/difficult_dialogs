import random
from logging import getLogger
from difficult_dialogs.statements import Statement

log = getLogger()

class BasePolicy(object):
    """ interaction with arguments """

    def __init__(self, name="base", argument=None):
        self.name = name
        self.current_statement = None
        self.current_assertion = None
        self._cache = []
        self.last_dialog = None
        self.finished = False
        self._in_agreement = True
        self.argument = argument

    def bind(self, argument):
        self.argument = argument
        self.argument.load()

    @property
    def cache(self):
        return self._cache

    @property
    def intro_statement(self):
        if self.argument is not None:
            return self.argument.intro_statement
        return ""

    @property
    def conclusion_statement(self):
        if self.argument is not None:
            return self.argument.conclusion_statement
        return ""

    @property
    def assertions(self):
        if self.argument is not None:
            return self.argument.assertions
        return []

    def reset(self):
        self._in_agreement = True
        self.current_assertion = None
        self.current_statement = None
        self._cache = []
        self.last_dialog = None
        self.finished = False

    def speak(self, text):
        """ format and cache output to not repeat """
        text = str(text).strip()
        self._cache_this(text)
        return text

    def start(self):
        """ prepare context of dialog

        at the minimum this should

        - reset policy, self.reset()
        - set running flag, self.finished = False
        - return speak intro statement

        """
        self.reset()
        self.finished = False
        return self.speak(self.intro_statement)

    def run(self):
        """ run the interaction """
        # introduce argument
        print(self.start())
        while not self.finished:
            try:
                # choose output
                output = self._run_once()
                if output is None:
                    # wait for output
                    continue
                print(output)
                # get user feedback
                if self.get_feedback():
                    self.agree()
                else:
                    self.disagree()
            except Exception as e:
                log.exception(e)
        # finish off argument
        print(self.end())

    def end(self):
        """ handle outcome of dialog

        at the minimum this should

        - unset running flag, self.finished = True
        - return speak conclusion statement

        """
        self.finished = True
        return self.speak(self.conclusion_statement)

    def is_cached(self, entry):
        entry = str(entry).strip()
        return entry in self.cache

    def _cache_this(self, entry):
        entry = str(entry).strip()
        self._cache.append(entry)

    def pick_assertion(self, argument=None):
        """ select which Premise to tackle next """
        argument = argument or self.argument
        choices = [t for t in argument.assertions
                   if not self.is_cached(t)]
        if not len(choices):
            return None
        assertion = random.choice(choices)
        self._cache_this(assertion)  # remember assertion
        return assertion

    def pick_next_statement(self, assertion=None):
        """ select which Statement to tackle next """
        assertion = assertion or self.current_assertion
        choices = [t for t in assertion.statements
                   if not self.is_cached(t)]
        if not len(choices):
            # go to next assertion
            next_assertion = self.pick_assertion()
            if next_assertion is None:
                self.finished = True
                return None  # no statements left
            self.current_assertion = next_assertion
            return self.pick_next_statement()
        statement = random.choice(choices)
        return statement

    def _run_once(self):
        # check if argument is fully exposed
        if self.finished:
            return None

        # check if we have an assertion
        if self.current_assertion is None:
            current_assertion = self.pick_assertion()
            self.current_assertion = current_assertion

        # pick action
        if not self._in_agreement:
            return self.on_negative_feedback()
        else:
            return self.on_positive_feedback()

    def agree(self):
        self._in_agreement = True

    def disagree(self):
        self._in_agreement = False

    def on_positive_feedback(self):
        """ react to positive feedback

        by default goes to next statement

        """
        self.agree()
        statement = self.pick_next_statement()
        if not statement:
            return None
        return self.speak(statement)

    def on_negative_feedback(self):
        """ react to negative feedback

        by default speak a support statement

        if no more support statements show the source

        if source was already shown, skip to next statement
        """
        self.disagree()
        statement = self.pick_next_statement()
        if not statement:
            return None
        return self.speak(statement)

    def _clean_prompt(self, prompt):
        prompt = prompt or "Do you agree with {{statement}} ?"
        if isinstance(prompt, list):
            prompt = random.choice(prompt)
        if self.current_statement is not None:
            current_statement = self.current_statement
        else:
            current_statement = "what i just said"
        prompt = prompt \
            .replace("{{statement}}", current_statement) \
            .replace("{statement}", current_statement) \
            .replace("{{ statement }}", current_statement) \
            .replace("{ statement }", current_statement)
        return prompt + " "

    def get_feedback(self, prompt=None):
        """
        ask user if he agrees with current statement or not

        prompt is a string or list of strings, if it's a list a random entry will be picked

        return True or False """
        prompt = self._clean_prompt(prompt)
        return "y" in input(prompt).lower()


class KnowItAllPolicy(BasePolicy):
    def __init__(self, argument):
        BasePolicy.__init__(self, name="KnowItAll", argument=argument)

    def on_negative_feedback(self):
        """ react to negative feedback

        by default speak a support statement

        if no more support statements show the source

        if source was already shown, skip to next statement
        """

        assertion = self.current_assertion

        # if no sources admit failure
        if not len(self.current_assertion.sources):
            self.agree()
            choices = ["I guess you are right",
                       "You may be right, i'll give it further thought",
                       "I'm not so sure anymore, i will think about it",
                       "I may be wrong"]
        else:
            self.disagree()
            choices = [t for t in assertion.support_statements
                       if not self.is_cached(t)]
        if not len(choices):
            # let's just show the sources
            source_str = "here is the source of my information\n"
            source_str += "\n".join(assertion.sources)
            if self.is_cached(source_str):
                self.agree()
                statement = "We will have to agree to disagree for now"
            else:
                statement = source_str
        else:
            statement = random.choice(choices)
        return self.speak(statement)
