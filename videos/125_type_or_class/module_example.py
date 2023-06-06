# See: https://docs.python.org/3/reference/datamodel.html

import sys
from types import ModuleType

class VerboseModule(ModuleType):
    def __setattr__(self, attr, value):
        print(f'Setting {attr}={value}')
        super().__setattr__(attr, value)


sys.modules[__name__].__class__ = VerboseModule

