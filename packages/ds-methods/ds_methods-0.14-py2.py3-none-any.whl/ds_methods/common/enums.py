from enum import Enum, EnumMeta


class BaseEnumMeta(EnumMeta):
    def __iter__(cls):
        return (member[1].value for member in cls.__members__.items())


class BaseEnum(Enum, metaclass=BaseEnumMeta):
    def __get__(self, instance, owner):
        return self.__class__.__members__[self.name].value

    @classmethod
    def validate(cls, x):
        return x in list(cls)
