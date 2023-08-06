__all__ = ['writable_property']


class writable_property(property):
    """writable property class"""

    def __init__(self, *args, **kw):
        super(writable_property, self).__init__(*args, **kw)
        for name in ['__doc__', '__module__', '__name__']:
            value = getattr(self.fget, name, None)
            setattr(self, name, value)

    def __get__(self, obj, type=None):
        if obj is None:
            return self
        if self.__name__ in obj.__dict__:
            return obj.__dict__[self.__name__]
        return super(writable_property, self).__get__(obj, type)

    def __set__(self, obj, value):
        try:
            super(writable_property, self).__set__(obj, value)
        except AttributeError:
            obj.__dict__[self.__name__] = value

    def __delete__(self, obj):
        try:
            super(writable_property, self).__delete__(obj)
        except AttributeError:
            obj.__dict__.pop(self.__name__, None)
