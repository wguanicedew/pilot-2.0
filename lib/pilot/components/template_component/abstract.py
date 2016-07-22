from ..component import Component as Base


class TemplateComponent(Base):
    def __init__(self, previous):
        Base.__init__(self, previous)
