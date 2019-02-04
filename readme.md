# Difficult Dialogs
[![Donate with Bitcoin](https://en.cryptobadges.io/badge/micro/1QJNhKM8tVv62XSUrST2vnaMXh5ADSyYP8)](https://en.cryptobadges.io/donate/1QJNhKM8tVv62XSUrST2vnaMXh5ADSyYP8)
[![Donate](https://img.shields.io/badge/Donate-PayPal-green.svg)](https://paypal.me/jarbasai)
<span class="badge-patreon"><a href="https://www.patreon.com/jarbasAI" title="Donate to this project using Patreon"><img src="https://img.shields.io/badge/patreon-donate-yellow.svg" alt="Patreon donate button" /></a></span>
[![Say Thanks!](https://img.shields.io/badge/Say%20Thanks-!-1EAEDB.svg)](https://saythanks.io/to/JarbasAl)

Tools to easily guide conversations towards a certain objective

- [Install](#install)
- [Usage](#usage)
  * [Sample output](#sample-output)
- [Documentation](#documentation)
  * [Statements](#statements)
  * [Premises](#premises)
  * [Arguments](#arguments)
  * [Policies](#policies)
- [Credits](#credits)

## Install

    pip install difficult_dialogs
    

## Usage

examples [here](https://github.com/JarbasAl/difficult_dialogs/tree/master/examples)

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

### Sample output

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

### Documentation

[Read the docs](https://jarbasal.github.io/difficult_dialogs/)

#### Statements

A statement is the lowest level of a dialog, it is a text sentence that may be True or False

```python
from difficult_dialogs.statements import Statement

s = Statement("i like pizza")

if s.is_true:
    print(s)

```

[Full docs](https://jarbasal.github.io/difficult_dialogs/difficult_dialogs.statements/)

#### Premises

A premise is a set of Statements, a premise is True if all it's statements are True

A premise also has sources to back it up, and support dialog that can be interjected at will

```python
from difficult_dialogs.premises import Premise

p = Premise("pizza tastes good", ["the taste of pizza is pleasant"])

for s in p.statements:
    print(s)

print(p.as_json)
"""
{'is_true': False,
 'sources': ['http://pizza_reviews.com'],
 'statements': ['pizza is food',
                'the taste of pizza is pleasant'  * [Install](#install)
10
  * [Usage](#usage)
11
    + [Sample output](#sample-output)
12
    + [Documentation](#documentation)
13
      - [Statements](#statements)
14
      - [Premises](#premises)
15
      - [Arguments](#arguments)
16
      - [Policies](#policies)],
 'support': ['i like pizza'],
 'description': 'pizza tastes good'}
 """
```

[Full docs](https://jarbasal.github.io/difficult_dialogs/difficult_dialogs.premises/)

#### Arguments

An Argument is a set of premises, a argument is True if all it's premises are True

Arguments can be loaded from a folder structured like this

```bash
$ tree argument_template/
argument_template/
├── argument.conclusion
├── argument.intro
├── X.premise
├── X.source
├── X.support
└── Y.premise

```

[Full docs](https://jarbasal.github.io/difficult_dialogs/difficult_dialogs.arguments/)

#### Policies

The actual dialog interaction between user/bot is created by a policy

Policies load an Argument and decide how the conversation will go

[Full docs](https://jarbasal.github.io/difficult_dialogs/difficult_dialogs.policy/)

You can make your own policies by overriding key methods, or you can
use the default policies

see [example of DummyPolicy](https://github.com/JarbasAl/difficult_dialogs/blob/master/examples/dummy_policy.py)

## Credits

[JarbasAl](https://jarbasal.github.io)