from collections.abc import Iterable


class Field(object):
    def __init__(self, pattern=None, required=False, null=False, default="not_set"):
        self.__dict__["pattern"] = pattern
        self.__dict__["required"] = required
        self.__dict__["null"] = null

        if default != "not_set":
            self.__dict__["default"] = default

    def __getitem__(self, item, default=None):
        return self.__dict__.get(item, default)

    def get(self, item, default=None):
        return self.__dict__.get(item, default)

    def __contains__(self, item):
        return item in self.__dict__


class IterableField(Field):
    def __init__(self, sub_pattern=None, required=False, null=False, default="not_set"):
        super().__init__(Iterable, required, null, default)
        self.__dict__["sub_pattern"] = sub_pattern

