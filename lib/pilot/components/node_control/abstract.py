from ..component import Component as Base


class NodeControl(Base):
    def __init__(self):
        Base.__init__(self)

    def setup_accounting(self):
        pass

    def prepare_payload(self):
        pass

    def submit_payload(self):
        pass

    def payload_setup_ipc(self):
        pass

    def verify_payload(self):
        pass
