from os.path import join, dirname

from difficult_dialogs.arguments import Argument
from difficult_dialogs.policy import BasePolicy

arg_folder = join(dirname(__file__), "argument_template")
arg = Argument(path=arg_folder)
dialog = BasePolicy(argument=arg)


# argument manual control
print(dialog.start())
while not dialog.finished:
    assertion = dialog.pick_assertion()
    if assertion:
        print(assertion)
        for s in assertion.statements:
            print(s)
        print(assertion.sources)
    else:
        print(dialog.end())
