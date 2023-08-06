#! /usr/bin/env python
from queue import Queue, Empty
from threading import Thread
import time
import logging
import os


logger = logging.getLogger("tlopo_executors.BlockingExecutor")


class BlockingExecutor:
    def __init__(self, concurrency=10):
        self.concurrency = concurrency
        self.run = False
        self.jobs = Queue(concurrency)
        self.control = Queue(concurrency)
        self.threads = []
        self.errors = []

    def start(self):
        self.run = True
        Thread(target=self.__run__).start()

    def stop(self):
        self.run = False

        while self.jobs.qsize() > 0:
            time.sleep(0.1)

        for t in self.threads:
            t.join()

    def add(self, job):
        if not self.run:
            raise Exception("Must start before adding job")

        self.jobs.put(job)

    def is_running(self):
        return self.jobs.qsize() > 0 and self.run

    def __run__(self):
        while self.run or self.jobs.qsize() > 0:
            job = None

            try:
                job = self.jobs.get()
            except Empty:
                time.sleep(0.5)

            if job != None:
                self.run_job(job)

    def run_job(self, job):
        def wrapper():
            self.control.put(None)

            try:
                job()
            except Exception as e:
                logger.exception(e)
                self.errors.append(e)

            self.control.get()

        t = Thread(target=wrapper)
        t.start()
        self.threads.append(t)
