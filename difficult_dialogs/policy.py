import random
from time import sleep
from threading import Thread
from logging import getLogger

log = getLogger("DialogRunner")


class BasePolicy(object):
    """ interaction with arguments """

    def __init__(self, name="base", argument=None):
        """

        Args:
            name:
            argument:
        """
        self.name = name
        self.current_statement = None
        self.current_premise = None
        self._cache = []
        self.last_dialog = None
        self.finished = False
        self._in_agreement = True
        self.argument = argument
        self._output = ""
        self._input = ""
        self._async_thread = None
        self._skip_feedback = False
        self._last_prompt = ""

    # lib
    def bind(self, argument):
        """

        Args:
            argument:
        """
        self.argument = argument
        self.argument.load()

    def reset(self):
        """

        """
        self._in_agreement = True
        self.current_premise = None
        self.current_statement = None
        self._cache = []
        self.last_dialog = None
        self.finished = False

    def speak(self, text):
        """
        - normalize text
        - cache response, self._cache_this(text)
        - manage output, self._output += text
        - return normalized text

         """
        text = str(text).strip()
        self._cache_this(text)
        if self._output and not self._output.endswith("\n"):
            self._output += "\n"
        self._output += text
        return text

    def is_cached(self, entry):
        """

        Args:
            entry:

        Returns:

        """
        entry = str(entry).strip()
        return entry in self.already_spoken

    def _cache_this(self, entry):
        """

        Args:
            entry:
        """
        entry = str(entry).strip()
        self._cache.append(entry)

    def _clean_prompt(self, prompt):
        """

        Args:
            prompt:

        Returns:

        """
        prompt = prompt or "Do you agree with {{statement}} ?"
        if isinstance(prompt, list):
            prompt = random.choice(prompt)
        if self.current_statement is not None:
            current_statement = self.current_statement.text.strip()
        else:
            current_statement = "what i just said"
        prompt = prompt \
            .replace("{{statement}}", current_statement) \
            .replace("{statement}", current_statement) \
            .replace("{{ statement }}", current_statement) \
            .replace("{ statement }", current_statement)
        return prompt + " "

    # dialog data
    @property
    def user_agrees(self):
        """

        Returns:

        """
        return self._in_agreement

    @property
    def already_spoken(self):
        """

        Returns:

        """
        return self._cache

    @property
    def output(self):
        """

        Returns:

        """
        return self._output

    @property
    def intro_statement(self):
        """

        Returns:

        """
        if self.argument is not None:
            return self.argument.intro_statement
        return ""

    @property
    def conclusion_statement(self):
        """

        Returns:

        """
        if self.argument is not None:
            return self.argument.conclusion_statement
        return ""

    @property
    def premises(self):
        """

        Returns:

        """
        if self.argument is not None:
            return self.argument.premises
        return []

    # dialog actions
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

    def end(self):
        """ handle outcome of dialog

        at the minimum this should

        - unset running flag, self.finished = True
        - return speak conclusion statement

        """
        self.finished = True
        return self.speak(self.conclusion_statement)

    def choose_premise(self, argument=None):
        """ select which Premise to tackle next """
        argument = argument or self.argument
        choices = [t for t in argument.premises
                   if not self.is_cached(t)]
        if not len(choices):
            return None
        assertion = random.choice(choices)
        self._cache_this(assertion)  # remember assertion
        return assertion

    def choose_next_statement(self, assertion=None):
        """ select which Statement to tackle next """
        assertion = assertion or self.current_premise
        choices = [t for t in assertion.statements
                   if not self.is_cached(t)]
        if not len(choices):
            # go to next assertion
            next_assertion = self.choose_premise()
            if next_assertion is None:
                self.finished = True
                return None  # no statements left
            self.current_premise = next_assertion
            return self.choose_next_statement()

        statement = random.choice(choices)
        self.current_statement = statement
        return statement

    def agree(self):
        """

        """
        self._in_agreement = True

    def disagree(self):
        """

        """
        self._in_agreement = False

    def what(self, default_answer="i don't know how to explain"):
        """ explain current statement """
        answer = default_answer
        choices = [t for t in self.current_premise.what
                   if not self.is_cached(t)]
        if len(choices):
            answer = random.choice(choices)
        return self.speak(answer)

    def why(self, default_answer="i don't know why"):
        """ explain cause of current statement """
        answer = default_answer
        choices = [t for t in self.current_premise.why
                   if not self.is_cached(t)]
        if len(choices):
            answer = choices[0]

        return self.speak(answer)

    def how(self, default_answer="i don't know how"):
        """ explain how current statement """
        answer = default_answer
        choices = [t for t in self.current_premise.how
                   if not self.is_cached(t)]
        if len(choices):
            answer = random.choice(choices)

        return self.speak(answer)

    def when(self, default_answer="i don't know when"):
        """ explain when current statement happened """
        answer = default_answer
        choices = [t for t in self.current_premise.when
                   if not self.is_cached(t)]
        if len(choices):
            answer = random.choice(choices)

        return self.speak(answer)

    def where(self, default_answer="i don't know where"):
        """ explain where current statement happened """
        answer = default_answer
        choices = [t for t in self.current_premise.where
                   if not self.is_cached(t)]
        if len(choices):
            answer = random.choice(choices)

        return self.speak(answer)

    def sources(self, default_answer="i don't remember where i learned this"):
        """ sources of current statement """
        answer = default_answer
        if len(self.current_premise.sources):
            answer = " ".join(self.current_premise.sources)
        return answer

    def skip_feedback(self):
        """

        """
        self._skip_feedback = True

    def reprompt(self):
        """

        Returns:

        """
        return self.speak(self._last_prompt)

    # sync
    def _run_once(self):
        """

        Returns:

        """
        # check if argument is fully exposed
        if self.finished:
            return None

        # check if we have an assertion
        if self.current_premise is None:
            current_assertion = self.choose_premise()
            self.current_premise = current_assertion

        # pick action
        if not self.user_agrees:
            return self.on_negative_feedback()
        else:
            return self.on_positive_feedback()

    def run(self):
        """ run the interaction, ask if user agrees or not after every
        statement

        NOTE: ignores on user input callback
        """
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
                if self.finished:
                    break
                # get user feedback
                if self._skip_feedback:
                    self._skip_feedback = False
                    continue
                if self.get_feedback():
                    self.agree()
                else:
                    self.disagree()

            except Exception as e:
                log.exception(e)
        # finish off argument
        print(self.end())

    def get_feedback(self, prompt=None):
        """
        used in run(), if running async wait_for_feedback is used instead

        ask user if he agrees with current statement or not

        prompt is a string or list of strings, if it's a list a random entry will be picked

        return True or False """
        prompt = self._clean_prompt(prompt)
        self._last_prompt = prompt
        return "y" in input(prompt).lower()

    # async
    def wait_for_input(self):
        """

        """
        self._input = ""
        while not self._input:
            sleep(0.5)

    def wait_for_feedback(self, prompt=None):
        """
        used in run_async(), if not running async get_feedback is used instead

        ask user if he agrees with current statement or not

        prompt is a string or list of strings, if it's a list a random entry will be picked

        return True or False """
        prompt = self._clean_prompt(prompt)
        self._output += "\n" + prompt
        self._last_prompt = prompt
        self.wait_for_input()
        return "y" in self._input.lower()

    def submit_input(self, text):
        """

        Args:
            text:
        """
        self._output = ""
        if self.on_user_input(text):
            self._input = text

    def run_async(self):
        """

        """
        self._async_thread = Thread(target=self._async_loop)
        self._async_thread.setDaemon(True)
        self._async_thread.start()

    def stop(self):
        """

        """
        self.finished = True
        try:
            self._async_thread.join()
            self._async_thread.cancel()
        except:
            pass
        self._async_thread = None

    def _async_loop(self):
        """ run the interaction async """
        # introduce argument
        self.start()
        while not self.finished:
            try:
                # choose output
                if not self._run_once():
                    continue

                if self._skip_feedback:
                    self._skip_feedback = False
                    continue
                # get user feedback
                if self.wait_for_feedback():
                    self.agree()
                else:
                    self.disagree()
            except Exception as e:
                log.exception(e)
        # finish off argument
        self.end()

    # events
    def on_user_input(self, text):
        """ handle user input

        intent parsing should be done here

        typical actions are

        - calling self.agree() or self.disagree() to direct the policy (return True)
        - calling self.what(), self.why(), self.how(), self.when(),
        self.where() and setting the output (return False)

        NOTE: only when running async

        return True or False, this determines if dialog should proceed or
        wait for different user input

        """
        return True

    def on_positive_feedback(self):
        """ react to positive feedback

        by default goes to next statement

        """
        statement = self.choose_next_statement()
        if not statement:
            return None
        return self.speak(statement)

    def on_negative_feedback(self):
        """ react to negative feedback

        by default speak a support statement

        if no more support statements show the source

        if source was already shown, skip to next statement
        """
        statement = self.choose_next_statement()
        if not statement:
            return None
        return self.speak(statement)


class KnowItAllPolicy(BasePolicy):
    """
    """
    def __init__(self, argument):
        """

        Args:
            argument:
        """
        BasePolicy.__init__(self, name="KnowItAll", argument=argument)

    def on_user_input(self, text):
        """ handle user input

        answers what, why, how, where, when questions or proceeds with dialog

        """
        if "what" in text:
            self.what()
            self.reprompt()
        elif "why" in text:
            self.why()
            self.reprompt()
        elif "how" in text:
            self.how()
            self.reprompt()
        elif "where" in text:
            self.where()
            self.reprompt()
        elif "when" in text:
            self.when()
            self.reprompt()
        else:
            return True
        return False

    def on_negative_feedback(self):
        """
        react to negative feedback

        usually you will take corrective action here and manage the dialog
        state

        to control the dialog loop you will typically use:
        - self.agree() / self.disagree()  - decide if on_negative_feedback
        or on_positive_feedback should be called
        - self.skip_feedback() - do not get user input

        by default speak a support statement

        if no more support statements call on_complete_failure
        """
        assertion = self.current_premise
        # comeback with support statement
        choices = [t for t in assertion.support_statements
                   if not self.is_cached(t)]

        if not len(choices):
            statement = self.on_complete_failure()
        else:
            statement = random.choice(choices)
        return self.speak(statement)

    def on_complete_failure(self):
        """
        handle failure to get a response, called by on_negative_feedback if
        no support statements available

        typically you will return a failure message and manage the dialog state

        to control the dialog loop you will typically use:
        - self.agree() / self.disagree()  - decide if on_negative_feedback
        or on_positive_feedback should be called
        - self.skip_feedback() - do not get user input

        Returns:
            sentence to speak (str)
        """
        if not len(self.current_premise.sources):
            # agree on failure
            self.agree()
            self.skip_feedback()
            choices = ["I guess you are right",
                       "You may be right, i'll give it further thought",
                       "I'm not so sure anymore, i will think about it",
                       "I may be wrong"]

        else:
            # let's just show the sources
            source_str = "here is the source of my information\n"
            source_str += "\n".join(self.current_premise.sources)

            choices = [source_str]
        choices = [c for c in choices if not self.is_cached(c)]
        if not len(choices):
            self.agree()
            self.skip_feedback()
            choices = ["We will have to agree to disagree for now"]
        return random.choice(choices)
