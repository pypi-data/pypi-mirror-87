from .blocking_executor import BlockingExecutor


class Executor:
    def __init__(self, jobs, concurrency=10):
        self.jobs = jobs
        self.exec = BlockingExecutor(concurrency)

    def run(self):
        self.exec.start()
        for job in self.jobs:
            self.exec.add(job)
        self.exec.stop()
        return self

    def success(self):
        return len(self.exec.errors) == 0

    def errors(self):
        return self.exec.errors
