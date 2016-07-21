from ..component import Component as Base


class SandboxSetup(Base):
    def __init__(self, previous):
        Base.__init__(self, previous)

    def establish_local_security(self):
        pass

    def fetch_node_information(self):
        pass

    def check_memory_limits(self):
        pass
