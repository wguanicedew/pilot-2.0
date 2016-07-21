from ..component import Component as Base


class PayloadControl(Base):
    def __init__(self, previous):
        Base.__init__(self, previous)

    def setup_accounting(self):
        pass

    def setup_payload(self):
        pass

    def execute_payload(self):
        pass

    def verify_output(self):
        pass
