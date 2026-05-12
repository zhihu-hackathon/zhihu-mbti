#!/usr/bin/env python
#-*- coding:utf-8 -*-

from concurrent.futures import ThreadPoolExecutor
from app.utils.log import get_logger

class User:
    def __init__(self, logger=None):
        if logger:
            self.logger = logger
        else:
            self.logger = get_logger(self.__class__.__name__)
    
    def submit_job(self):
        self.executor.submit(self.job_detail)
    
    def job_detail(self):
        self.logger.info('job runs')