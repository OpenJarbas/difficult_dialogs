from os.path import join, dirname

from difficult_dialogs.arguments import Argument

arg_folder = join(dirname(__file__), "i_think_therefore_i_am")
arg = Argument(arg_folder)

# argument data
all_statements = arg.all_statements()
all_support_statements = arg.all_support()
all_sources = arg.all_sources()
intro = arg.intro_statement
conclusion = arg.conclusion_statement


# argument / user loop
debug = False

if debug:
    print("ARGUING IN FAVOR OF:", arg.name)
    print("---ARGUMENT INTRO")
print("BOT:", arg.start())
while not arg.finished:
    if debug:
        print("---NEXT ASSERTION")

    print("BOT:", arg.next_statement())
    if debug:
        print("__ARGUING IN FAVOR OF: ", arg.current_statement)
    user = input("do you agree?  USER: ")
    while "y" not in user:
        support = arg.support()

        if not support:
            if debug:
                print("---OUT OF ARGUMENTS")
            source = arg.source()
            if source:
                if debug:
                    print("---ASSERTION SOURCES")
                print("BOT:", "here is the source of my information",
                      "\n" + arg.source())
                print("BOT:", "we will need to agree to disagree")
            else:
                if debug:
                    print("---NO SOURCES")
                print("BOT:", "i guess you're right")
            user = "y"
        else:
            if debug:
                print("---ASSERTION SUPPORT ARGUMENT")
            print("BOT:", support)
            user = input("do you agree?  USER: ")
