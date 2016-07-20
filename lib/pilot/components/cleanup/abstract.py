from ..component import Component as Base


class Cleanup(Base):
    def __init__(self):
        Base.__init__(self)

    def controller_cleanup(self):
        pass

    def pilot_cleanup(self):
        pass
