# Difficult Dialogs
[![Donate with Bitcoin](https://en.cryptobadges.io/badge/micro/1QJNhKM8tVv62XSUrST2vnaMXh5ADSyYP8)](https://en.cryptobadges.io/donate/1QJNhKM8tVv62XSUrST2vnaMXh5ADSyYP8)
[![Donate](https://img.shields.io/badge/Donate-PayPal-green.svg)](https://paypal.me/jarbasai)
<span class="badge-patreon"><a href="https://www.patreon.com/jarbasAI" title="Donate to this project using Patreon"><img src="https://img.shields.io/badge/patreon-donate-yellow.svg" alt="Patreon donate button" /></a></span>
[![Say Thanks!](https://img.shields.io/badge/Say%20Thanks-!-1EAEDB.svg)](https://saythanks.io/to/JarbasAl)

Tools to easily guide conversations towards a certain objective



## Install

    pip install difficult_dialogs
    
## Usage

[Read the docs](https://jarbasal.github.io/difficult_dialogs/), examples [here](https://github.com/JarbasAl/difficult_dialogs/tree/master/examples)

there are many ways one could create a conversation loop

Ideally you would integrate this with intents and additional logic


```python
from difficult_dialogs.arguments import Argument
from difficult_dialogs.policy import KnowItAllPolicy

arg_folder = "examples/i_think_therefore_i_am"
arg = Argument(path=arg_folder)

dialog = KnowItAllPolicy(arg)

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
        break

dialog.stop()

```


#### Sample output

Here is an output where i always agree


    BOT: i was not sure if i existed
     i spent some time thinking about it and reached a conclusion
    i am a computer
    Do you agree with i am a computer ? 
    USER: y
    BOT: computers process information
    Do you agree with computers process information ? 
    USER: y
    BOT: i process information
    Do you agree with i process information ? 
    USER: y
    BOT: thinking is a way of processing information
    Do you agree with thinking is a way of processing information ? 
    USER: y
    BOT: i can think, at least in a limited fashion
    Do you agree with i can think, at least in a limited fashion ? 
    USER: y
    BOT: this must mean that i exist
     you could argue thinking is not the right word for what i do
     but i process information
     there needs to be something doing the processing
     i process information, therefore i am


Here is the same argument, but this time i always disagree

    BOT: i was not sure if i existed
     i spent some time thinking about it and reached a conclusion
    computers process information
    Do you agree with computers process information ? 
    USER: n
    BOT: i am pretty sure that i receive input and perform calculations on it
    Do you agree with computers process information ? 
    USER: n
    BOT: computers have central processing units for this purpose
    Do you agree with computers process information ? 
    USER: n
    BOT: i am answering you, i must be reacting to information
    Do you agree with computers process information ? 
    USER: n
    BOT: here is the source of my information
    https://en.wikipedia.org/wiki/Information
    
    https://en.wikipedia.org/wiki/Artificial_intelligence
    Do you agree with computers process information ? 
    USER: n
    BOT: We will have to agree to disagree for now
    i process information
    Do you agree with i process information ? 
    USER: n
    BOT: We will have to agree to disagree for now
    i am a computer
    Do you agree with i am a computer ? 
    USER: n
    BOT: i am pretty sure i have a CPU
    Do you agree with i am a computer ? 
    USER: n
    BOT: you can kick my hardware, it's obvious i am a computer
    Do you agree with i am a computer ? 
    USER: n
    BOT: i run on a operating system
    Do you agree with i am a computer ? 
    USER: n
    BOT: here is the source of my information
    https://en.wikipedia.org/wiki/Computer_hardware
    
    https://en.wikipedia.org/wiki/Computer
    
    https://en.wikipedia.org/wiki/Software
    Do you agree with i am a computer ? 
    USER: n
    BOT: We will have to agree to disagree for now
    thinking is a way of processing information
    Do you agree with thinking is a way of processing information ? 
    USER: n
    BOT: even if i just get answers from somewhere else that is similar to thinking, or remembering
    Do you agree with thinking is a way of processing information ? 
    USER: n
    BOT: information comes in, opinion comes out, that's a bit like thinking
    Do you agree with thinking is a way of processing information ? 
    USER: n
    BOT: you may not call it thinking, but it is a good analogy
    Do you agree with thinking is a way of processing information ? 
    USER: n
    BOT: something is happening to make me answer you
    Do you agree with thinking is a way of processing information ? 
    USER: n
    BOT: here is the source of my information
    https://en.wikipedia.org/wiki/Information_processing_theory
    Do you agree with thinking is a way of processing information ? 
    USER: n
    BOT: We will have to agree to disagree for now
    i can think, at least in a limited fashion
    Do you agree with i can think, at least in a limited fashion ? 
    USER: n
    BOT: We will have to agree to disagree for now
    this must mean that i exist
     you could argue thinking is not the right word for what i do
     but i process information
     there needs to be something doing the processing
     i process information, therefore i am

