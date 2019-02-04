from os.path import join, dirname
import random
from time import sleep
from difficult_dialogs.arguments import Argument
from difficult_dialogs.policy import KnowItAllPolicy


class DummyPolicy(KnowItAllPolicy):
    """
    """
    def __init__(self, argument):
        """

        Args:
            argument:
        """
        KnowItAllPolicy.__init__(self, argument)
        self.name = "dummy_policy"

    def on_user_input(self, text):
        """ handle user input

        intent parsing should be done here

        typical actions are

        - calling self.agree() or self.disagree() to direct the policy
        - calling self.what(), self.why(), self.how(), self.when(),
        self.where() to answer the Five Ws
        - calling self.reprompt() to get back on topic

        return True or False, this determines if dialog should proceed or
        wait for different user input

        """
        print("USER: " + text)
        # returning False will ignore the user input
        # useful to intercept and handle text in your own way
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

    def wait_for_feedback(self, prompt=None):
        """
        ask user if he agrees with current statement or not

        prompt is a string or list of strings

        return True or False """
        agrees = random.choice([True, False])
        if agrees:
            self.submit_input("I agree")
            return True
        self.submit_input("I disagree")
        return False

    def get_feedback(self, prompt=None):
        """
        used in run(), if running async wait_for_feedback is used instead

        ask user if he agrees with current statement or not

        prompt is a string or list of strings, if it's a list a random entry will be picked

        return True or False """
        agrees = random.choice([True, False])
        if agrees:
            print("USER: I agree")
            return True
        print("USER: I disagree")
        return False

    def on_positive_feedback(self):
        """ react to positive feedback

        go to next statement or end the conversation

        typically you want to return self.speak(statement)

        :return statement (str) or None

        """
        statement = self.choose_next_statement()
        if not statement:
            return None
        return self.speak(statement)

    def on_negative_feedback(self):
        """
        react to negative feedback

        usually you will take corrective action here and manage the dialog
        state

        to control the dialog loop you will typically use:
        - self.agree() / self.disagree()  - decide if on_negative_feedback
        or on_positive_feedback should be called
        - self.skip_feedback() - do not get user input

        typically you want to return self.speak(statement) or None to end
        the conversation

        :return statement (str) or None

        """
        # no idea what to do
        return self.speak(self.on_complete_failure())

    def start(self):
        """ prepare context of dialog

        at the minimum this should

        - reset policy, self.reset()
        - set running flag, self.finished = False
        - return speak intro statement

        """
        self.reset()
        self.finished = False
        return self.speak("i am starting, this is the intro")

    def end(self):
        """ handle outcome of dialog

        at the minimum this should

        - unset running flag, self.finished = True
        - return speak conclusion statement

        """
        self.finished = True
        if self.user_agrees:
            return self.speak("finished dialog, this is the conclusion")
        else:
            return self.speak("too bad we don't agree")

    def on_complete_failure(self):
        """
        handle failure to get a response, called by on_negative_feedback if
        no support statements available

        typically you will return a failure message and manage the dialog state

        to control the dialog loop you will typically use:
        - self.agree() / self.disagree()  - decide if on_negative_feedback
        or on_positive_feedback should be called
        - self.skip_feedback() - do not get user input

        typically you want to return self.speak(statement) or None to end
        the conversation

        Returns:
            sentence to speak (str)
        """
        # abort the dialog
        self.finished = True
        self.skip_feedback()
        return "fatal error 404, answer not found"

    def speak(self, text):
        """
        - normalize text
        - cache response, self._cache_this(text)
        - manage output, self._output += text
        - return normalized text

         """
        text = str(text).strip()
        self._cache_this(text)
        if self._async_thread is not None:
            print("BOT: " + text)
            return text
        return "BOT: " + text


arg_folder = join(dirname(__file__), "argument_template")
arg = Argument(path=arg_folder)

# ignore user input, just go trough all premises
# dialog = BasePolicy(arg)

# defend when user disagrees
dialog = DummyPolicy(arg)

# dialog.run()

# argument / user loop
dialog.run_async()
while not dialog.finished:
    sleep(1)

dialog.stop()
