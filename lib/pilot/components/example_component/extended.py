from .default import ExampleComponent as Base


class ExampleComponent(Base):
    def __init__(self, previous):
        Base.__init__(self, previous)

    def foo(self):
        print("this is extended")
        Base.foo(self)
