from .abstract import ExampleComponent as Base


class ExampleComponent(Base):
    def __init__(self, previous):
        Base.__init__(self, previous)
