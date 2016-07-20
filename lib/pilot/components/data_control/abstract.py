from ..component import Component as Base


class DataControl(Base):
    def __init__(self):
        Base.__init__(self)

    def replica_lookup(self):
        pass

    def stage_in(self):
        pass

    def stage_out(self):
        pass
