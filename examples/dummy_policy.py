from os.path import join, dirname
import time
from difficult_dialogs.arguments import Argument
from difficult_dialogs.policy import KnowItAllPolicy


class DummyPolicy(KnowItAllPolicy):
    def __init__(self, argument):
        KnowItAllPolicy.__init__(self, argument)
        self.name = "dummy_policy"

    def get_feedback(self, prompt=None):
        """
        ask user if he agrees with current statement or not

        prompt is a string or list of strings, if it's a list a random entry will be picked

        return True or False """
        if int(time.time() % 2)== 0:
            print(self.speak("user agrees"))
            return True
        print(self.speak("user disagrees"))
        return False

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

        self.finished = True
        return "aborting dialog"

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
        return self.speak("finished dialog, this is the conclusion")


arg_folder = join(dirname(__file__), "argument_template")
arg = Argument(path=arg_folder)

# ignore user input, just go trough all premises
# dialog = BasePolicy(arg)

# defend when user disagrees
dialog = DummyPolicy(arg)


# argument / user loop
dialog.run()
