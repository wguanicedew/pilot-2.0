from ..component import Component as Base


class ExampleComponent(Base):
    def __init__(self, previous=None):
        Base.__init__(self, previous)
        print("loading component")
        if previous:
            print("previous was " + previous.__class__.__module__)
        else:
            print("this is first one")

    def __switch__(self):
        print("Switching component")

    def foo(self):
        print('this is test in abstract from ' + self.__class__.__module__)
