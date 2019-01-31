# Difficult Dialogs
[![Donate with Bitcoin](https://en.cryptobadges.io/badge/micro/1QJNhKM8tVv62XSUrST2vnaMXh5ADSyYP8)](https://en.cryptobadges.io/donate/1QJNhKM8tVv62XSUrST2vnaMXh5ADSyYP8)
[![Donate](https://img.shields.io/badge/Donate-PayPal-green.svg)](https://paypal.me/jarbasai)
<span class="badge-patreon"><a href="https://www.patreon.com/jarbasAI" title="Donate to this project using Patreon"><img src="https://img.shields.io/badge/patreon-donate-yellow.svg" alt="Patreon donate button" /></a></span>
[![Say Thanks!](https://img.shields.io/badge/Say%20Thanks-!-1EAEDB.svg)](https://saythanks.io/to/JarbasAl)

Tool to easily guide conversations towards a certain objective


## Arguments

Arguments are created by structuring a folder like this

    $ tree argument_template/
    argument_template/
    ├── argument.conclusion
    ├── argument.intro
    ├── statement_0.dialog
    ├── statement_0.source
    ├── statement_0.support
    └── statement_1.dialog


- folder name is the argument name

- X.dialog is an assertion the argument depends on

- X.support are "comebacks" for when user disagrees with assertion

- X.source is information source for the assertion

- X is the assertion we are currently arguing for

#### working principle:

- argument.intro is printed fully on start, it is meant to introduce the argument

- a .dialog file will be picked randomly and read

- all statements inside a .dialog file will be read, but in a random order

- no statements will be repeated

- when all statements inside a .dialog file are read, another .dialog file will be picked

- when all .dialog files are read, argument.conclusion is printed fully, it is meant to deliver the conclusion we want to reach

#### Sample output

there are many ways one could create a conversation loop, ideally you would 
integrate this with intents and additional logic

the simplest logic would be to check if the user agrees or not with a 
statement, and skip information based on that.

Here is an output where i always agree

    BOT: i was not sure if i existed
     i spent some time thinking about it and reached a conclusion
    BOT: i am a computer
    do you agree?  USER: y
    BOT: i can think, at least in a limited fashion
    do you agree?  USER: y
    BOT: thinking is a way of processing information
    do you agree?  USER: y
    BOT: i process information
    do you agree?  USER: y
    BOT: computers process information
    do you agree?  USER: y
    BOT: this must mean that i exist
     you could argue thinking is not the right word for what i do
     but i process information
     there needs to be something doing the processing
     i process information, therefore i am
     
Here is the same argument, but this time i always disagree

    BOT: i was not sure if i existed
     i spent some time thinking about it and reached a conclusion
    BOT: i am a computer
    do you agree?  USER: no
    BOT: i run on a operating system
    do you agree?  USER: no
    BOT: i am pretty sure i have a CPU
    do you agree?  USER: no
    BOT: you can kick my hardware, it's obvious i am a computer
    do you agree?  USER: no
    BOT: here is the source of my information 
    https://en.wikipedia.org/wiki/Computer_hardware
    
    https://en.wikipedia.org/wiki/Computer
    
    https://en.wikipedia.org/wiki/Software
    BOT: we will need to agree to disagree
    BOT: thinking is a way of processing information
    do you agree?  USER: no
    BOT: something is happening to make me answer you
    do you agree?  USER: no
    BOT: you may not call it thinking, but it is a good analogy
    do you agree?  USER: no
    BOT: even if i just get answers from somewhere else that is similar to thinking, or remembering
    do you agree?  USER: no
    BOT: information comes in, opinion comes out, that's a bit like thinking
    do you agree?  USER: no
    BOT: here is the source of my information 
    https://en.wikipedia.org/wiki/Information_processing_theory
    
    https://en.wikipedia.org/wiki/Cogito,_ergo_sum
    BOT: we will need to agree to disagree
    BOT: i can think, at least in a limited fashion
    do you agree?  USER: no
    BOT: here is the source of my information 
    https://en.wikipedia.org/wiki/Information_processing_theory
    
    https://en.wikipedia.org/wiki/Cogito,_ergo_sum
    BOT: we will need to agree to disagree
    BOT: computers process information
    do you agree?  USER: no
    BOT: i am pretty sure that i receive input and perform calculations on it
    do you agree?  USER: no
    BOT: computers have central processing units for this purpose
    do you agree?  USER: no
    BOT: i am answering you, i must be reacting to information
    do you agree?  USER: no
    BOT: here is the source of my information 
    https://en.wikipedia.org/wiki/Information
    
    https://en.wikipedia.org/wiki/Artificial_intelligence
    BOT: we will need to agree to disagree
    BOT: i process information
    do you agree?  USER: no
    BOT: here is the source of my information 
    https://en.wikipedia.org/wiki/Information
    
    https://en.wikipedia.org/wiki/Artificial_intelligence
    BOT: we will need to agree to disagree
    BOT: this must mean that i exist
     you could argue thinking is not the right word for what i do
     but i process information
     there needs to be something doing the processing
     i process information, therefore i am
    do you agree?  USER: no
    BOT: i guess you're right

## Install

    pip install difficult_dialogs
    
## Usage

More examples [here](/examples)


Load an argument from a folder

    from difficult_dialogs.arguments import Argument
    
    arg_folder = join(dirname(dirname(__file__)),
                      "examples", "i_think_therefore_i_am")
    arg = Argument(arg_folder)
    

    print("ARGUING IN FAVOR OF:", arg.name)
    print("---ARGUMENT INTRO")
    print("BOT:", arg.start())
    while not arg.finished:
        print("---NEXT ASSERTION")

        print("BOT:", arg.next_statement())
        print("__ARGUING IN FAVOR OF: ", arg.current_statement)
        user = input("do you agree?  USER: ")
        while "y" not in user:
            support = arg.support()

            if not support:
                print("---OUT OF ARGUMENTS")
                source = arg.source()
                if source:
                    print("---ASSERTION SOURCES")
                    print("BOT:", "here is the source of my information",
                          "\n" + arg.source())
                    print("BOT:", "we will need to agree to disagree")
                else:
                    print("---NO SOURCES")
                    print("BOT:", "i guess you're right")
                user = "y"
            else:
                print("---ASSERTION SUPPORT ARGUMENT")
                print("BOT:", support)
                user = input("do you agree?  USER: ")

