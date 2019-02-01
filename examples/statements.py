from difficult_dialogs.statements import Statement

s = Statement("i like pizza")
assert str(s) == "i like pizza"
assert s.text == "i like pizza"

assert bool(s) == True
s.disagree()
assert bool(s) == False
s.agree()
assert bool(s) == True
