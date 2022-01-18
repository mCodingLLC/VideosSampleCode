##################
# Homework (easy): write plugin/tests to forbid calling 'eval' anywhere:
eval('print("this should be a lint error!")')

# Don't worry about nefarious cases like:
globals()['__builtins__']['e' + 'val']("print('sneaky call to eval')")

f = eval
f('print("another sneaky eval")')


##################
# Homework (easy): write plugin/tests to forbid creating metaclasses
# (any class inheriting from 'type'):

class MyMeta(type):  # forbidden!
    pass


##################
# Homework (more involved): write plugin/tests to forbid this:
a, b = a[:] = [[]], []  # forbidden!

# disallow any name from appearing in multiple targets
# e.g. in this 'a' was used twice
