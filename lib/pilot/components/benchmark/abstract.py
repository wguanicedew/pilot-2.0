from ..component import Component as Base


class Benchmark(Base):
    def __init__(self, previous):
        Base.__init__(self, previous)

    def evaluate_execution_environment_speed(self):
        pass
