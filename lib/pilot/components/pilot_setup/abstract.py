from ..component import Component as Base


class PilotSetup(Base):
    def __init__(self):
        Base.__init__(self)

    def establish_signal_handling(self):
        pass

    def retrieve_configuration(self):
        pass

    def setup_local_environment(self):
        pass
