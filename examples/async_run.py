from os.path import join, dirname

from difficult_dialogs.arguments import Argument
from difficult_dialogs.policy import KnowItAllPolicy, BasePolicy

arg_folder = join(dirname(__file__), "i_think_therefore_i_am")
arg = Argument(path=arg_folder)

# ignore user input, just go trough all premises
# dialog = BasePolicy(argument=arg)

# defend when user disagrees
dialog = KnowItAllPolicy(arg)


# argument / user loop
dialog.run_async()

while True:
    try:
        if dialog.output:
            print("BOT: " + dialog.output)
            if not dialog.finished:
                utterance = input("USER: ")
                dialog.submit_input(utterance)
            else:
                break
    except KeyboardInterrupt:
        dialog.finished = True
        break

dialog.stop()

