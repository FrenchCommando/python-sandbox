"""
__getattribute__ is called on top of every call of self.item
first check if there is a corresponding @property
if not or raises an AttributeError (other errors are not caught),
-> checks for __getattr__
__getattr__ should raise AttributeError, otherwise it returns None
"""


class DictClass:
    def __init__(self, d):
        # print(self.c) -> infinite recursion because looking for field _d
        self._d = d
        # self.c = "From constructor"
        # print(self.random_name)
        print(self.c)
        self.later_c = "I'm here"
        print(self.c)

    @property
    def c(self):
        raise AttributeError("Calling c failed")
        return self.later_c
        return "my_property"

    def __getattr__(self, item):
        if item in self._d:
            return self._d[item]
        raise AttributeError("Neither {} nor {} has attribute {}".format(self, self._d, item))
