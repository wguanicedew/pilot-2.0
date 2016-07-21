from ..component import Component as Base


class Heartbeat(Base):
    def __init__(self, previous):
        Base.__init__(self, previous)

    def measure_execution_parameters(self):
        """
        Measure memory, CPU usage, execution time...
        :return:
        """
        pass

    def submit_measurement_to_central(self):
        pass
