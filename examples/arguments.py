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