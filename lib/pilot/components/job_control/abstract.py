from ..component import Component as Base


class JobControl(Base):
    def __init__(self, previous):
        Base.__init__(self, previous)

    def get_jobs_from_scheduler(self):
        pass

    def validate_job_vs_available_resources(self):
        pass
