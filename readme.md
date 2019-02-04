# Difficult Dialogs
[![Donate with Bitcoin](https://en.cryptobadges.io/badge/micro/1QJNhKM8tVv62XSUrST2vnaMXh5ADSyYP8)](https://en.cryptobadges.io/donate/1QJNhKM8tVv62XSUrST2vnaMXh5ADSyYP8)
[![Donate](https://img.shields.io/badge/Donate-PayPal-green.svg)](https://paypal.me/jarbasai)
<span class="badge-patreon"><a href="https://www.patreon.com/jarbasAI" title="Donate to this project using Patreon"><img src="https://img.shields.io/badge/patreon-donate-yellow.svg" alt="Patreon donate button" /></a></span>
[![Say Thanks!](https://img.shields.io/badge/Say%20Thanks-!-1EAEDB.svg)](https://saythanks.io/to/JarbasAl)

Tools to easily guide conversations towards a certain objective

## Install

    pip install difficult_dialogs
    
## Usage

More examples [here](/examples)

there are many ways one could create a conversation loop

Ideally you would integrate this with intents and additional logic

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


### Policies

A policy is a way to run an argument, it decides how the conversation will go

You can make your own policies by overriding key methods, or you can use the default policies 

see [example of DummyPolicy](examples/dummy_policy.py)

- argument.intro is printed fully on start, it is meant to introduce the argument

- a .premise file will be picked randomly and read

- all statements inside a .premise file will be read, but in a random order

- no statements will be repeated

- when all statements inside a .premise file are read, another .premise file will be picked

- when all .premise files are read, argument.conclusion is printed fully, it is meant to deliver the conclusion we want to reach

```python
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
```

You also have access to lower level details, policies can be used outside the run() loop

```python
from os.path import join, dirname

from difficult_dialogs.arguments import Argument
from difficult_dialogs.policy import BasePolicy

arg_folder = join(dirname(__file__), "argument_template")
arg = Argument(path=arg_folder)
dialog = BasePolicy(argument=arg)

# argument manual control
print(dialog.start())
while not dialog.finished:
    assertion = dialog.choose_premise()
    if assertion:
        print(assertion)
        for s in assertion.statements:
            print(s)
        print(assertion.sources)
    else:
        print(dialog.end())
```
### Arguments

An Argument is a set of premises, a argument is True if all it's premises are True

Arguments can be loaded from file structuring a folder like this

    $ tree argument_template/
    argument_template/
    ├── argument.conclusion
    ├── argument.intro
    ├── X.premise
    ├── X.source
    ├── X.support
    └── Y.premise


- folder name is the argument name

- X.premise is a premise the argument depends on

- X.support are "comebacks" for when user disagrees with premise

- X.source is information source for the premise

- X is the premise we are currently arguing for

```python
from difficult_dialogs.arguments import Argument
from os.path import dirname, join

arg = Argument()

path = join(dirname(__file__), "argument_template")
arg.load(path)

assert arg.is_true
assert arg.description == "argument_template"

from pprint import pprint

pprint(arg.as_json)

"""
       {'conclusion': 'this concludes my argument that Z is indeed True\n'
                      ' i will use the next line to tell you something extra\n'
                      ' here is more info\n'
                      ' goodbye and thank you\n'
                      ' this file was a single message',
        'intro': 'here i introduce the topic\n'
                 ' all lines in intro file are printed\n'
                 ' this is a single message about X\n'
                 ' topic introduced successfully',
        'is_true': True,
        'premises': [{'description': 'Y',
                      'is_true': True,
                      'sources': [],
                      'statements': [
                          'when all statements are said i will tell you '
                          'the conclusion\n',
                          'statements are not dependent on each other'],
                      'support': []},
                     {'description': 'X',
                      'is_true': True,
                      'sources': ['http://SOURCE_CODE.com\n',
                                  'http://SCIENTIFIC_PAPER.net\n',
                                  'https://WIKIPEDIA.ORG'],
                      'statements': [
                          'statements in .premise files are said in random '
                          'order\n',
                          'i will say this exactly once\n',
                          'i will say all sentences in .premise files'],
                      'support': ['this works the same way as .premise\n',
                                  'i am spoken when you disagree with X\n',
                                  'X is True because i say so']}]
        }
"""

```


### Premises

A premise is a set of Statements, a premise is True if all it's statements are True

A premise also has sources to back it up, and support dialog that can be interjected at will

```python
from difficult_dialogs.premises import Premise

p = Premise("pizza tastes good")
p.add_statement("pizza is food")
p.add_statement("the taste of pizza is pleasant")
p.add_support_statement("i like pizza")
p.add_source("http://pizza_reviews.com")

for s in p.statements:
    assert s.is_true
assert bool(p) == True

p.statements[0].disagree()

assert bool(p) == False

assert p.as_json == {'is_true': False,
                     'sources': ['http://pizza_reviews.com'],
                     'statements': ['pizza is food',
                                    'the taste of pizza is pleasant'],
                     'support': ['i like pizza'],
                     'description': 'pizza tastes good'}
```


### Statements

A statement is the lowest level of a dialog, it is a text sentence that may be True or False

```python
from difficult_dialogs.statements import Statement

s = Statement("i like pizza")
assert str(s) == "i like pizza"
assert s.text == "i like pizza"

assert bool(s) == True
s.disagree()
assert bool(s) == False
s.agree()
assert bool(s) == True
```
