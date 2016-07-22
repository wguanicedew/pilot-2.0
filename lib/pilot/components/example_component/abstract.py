from ..component import Component as Base


class ExampleComponent(Base):
    def __init__(self, previous=None):
        Base.__init__(self, previous)
        self.a = 'prop test'
        print("loading component")
        if previous:
            print("previous was " + previous.__class__.__module__)
        else:
            print("this is first one")

    def __switch__(self):
        print("Switching component")

    def foo(self):
        print('this is test in abstract from ' + self.__class__.__module__)

    def ti(self, *args):
        print('self is from ' + self.__module__)
        print("args len: %d" % len(args))

    @classmethod
    def ci(cls, *args):
        print('class is from ' + cls.__module__)
        print("args len: %d" % len(args))

    @staticmethod
    def si(*args):
        print("static\nargs len: %d" % len(args))

    @property
    def prop(self):
        print('prop self is from ' + self.__module__)
        return self.a

    @prop.setter
    def prop(self, arg):
        print('prop self is from ' + self.__module__)
        self.a = arg

    def __getattr__(self, name):
        print "getting attr from " + self.__module__
        try:
            return object.__getattribute__(self, name)
        except AttributeError:
            return None

    def __setattr__(self, name, arg):
        print "setting attr to " + self.__module__
        try:
            return object.__setattr__(self, name, arg)
        except AttributeError:
            pass
