#/usr/bin/env python
# -*- coding:utf-8 -*-

import logging

logging.basicConfig(
    level=logging.WARNING,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
    )

def get_logger(name):
    return logging.getLogger(name)