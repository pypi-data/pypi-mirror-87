#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging

def get_logger(name='sofart'):
    logger = logging.getLogger(name)
    ch = logging.StreamHandler()
    logger.setLevel(logging.INFO)
    ch.setLevel(logging.INFO)
    logger.addHandler(ch)
    logger.disabled = True
    return logger
