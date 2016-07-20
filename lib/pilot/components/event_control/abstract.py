from ..component import Component as Base


class EventControl(Base):
    def __init__(self):
        Base.__init__(self)

    def get_event_ranges(self):
        pass

    def update_events(self):
        pass
