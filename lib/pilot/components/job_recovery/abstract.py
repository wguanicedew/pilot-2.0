from ..component import Component as Base


class JobRecovery(Base):
    def __init__(self):
        Base.__init__(self)

    def find_old_unstaged_jobs(self):
        pass

    def stage_out_files(self):
        pass

    def cleanup(self):
        pass
