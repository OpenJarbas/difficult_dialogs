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
