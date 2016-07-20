from ..component import Component as Base


class JobControl(Base):
    def __init__(self):
        Base.__init__(self)

    def get_jobs_from_scheduler(self):
        pass

    def validate_job_vs_available_resources(self):
        pass
