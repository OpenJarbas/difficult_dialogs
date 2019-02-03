from os.path import join, dirname

from difficult_dialogs.arguments import Argument
from difficult_dialogs.policy import BasePolicy

arg_folder = join(dirname(__file__), "i_think_therefore_i_am")
arg = Argument(path=arg_folder)
dialog = BasePolicy(argument=arg)


# load a random premise
assertion = dialog.choose_premise()
dialog.current_premise = assertion

print(assertion)
print(assertion.sources)

# select a statement from premise
statement = dialog.choose_next_statement()
print(statement)


# argument manual control

arg_folder = join(dirname(__file__), "argument_template")
arg = Argument(path=arg_folder)
dialog = BasePolicy(argument=arg)
print(dialog.start())

while not dialog.finished:
    # get a new premise
    assertion = dialog.choose_premise()
    if assertion:
        for s in assertion.statements:
            print(s)
    else:
        # no more premises
        print(dialog.end())
