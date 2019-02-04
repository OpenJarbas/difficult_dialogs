from os.path import join, dirname

from difficult_dialogs.arguments import Argument
from difficult_dialogs.policy import KnowItAllPolicy


class DebugPolicy(KnowItAllPolicy):
    """
    """
    def __init__(self, argument):
        """

        Args:
            argument:
        """
        KnowItAllPolicy.__init__(self, argument)
        self.name = "debug_policy"

    def run(self):
        """ run the interaction """
        # introduce argument
        print("## ARGUMENT START: " + str(self.argument))
        print(self.start())
        while not self.finished:
            topic = str(self.current_premise)
            print("## Currently discussing: " + topic)
            # choose output
            output = self._run_once()
            if output is None:
                # wait for output
                continue
            print("BOT: " + output)
            # get user feedback
            if self.get_feedback():
                self.agree()
            else:
                self.disagree()

        # finish off argument
        print("## ARGUMENT CONCLUSION")
        print(self.end())

    def get_feedback(self, prompt=None):
        """
        ask user if he agrees with current statement or not

        prompt is a string or list of strings, if it's a list a random entry will be picked

        return True or False """
        prompt = self._clean_prompt(prompt)
        prompt = "USER: " + prompt
        return "y" in input(prompt).lower()


arg_folder = join(dirname(__file__), "i_think_therefore_i_am")
arg = Argument(path=arg_folder)

# ignore user input, just go trough all premises
# dialog = BasePolicy(arg)

# defend when user disagrees
dialog = DebugPolicy(arg)


# argument / user loop
dialog.run()
