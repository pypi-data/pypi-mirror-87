# -*- coding: utf-8 -*-

import multiprocessing

from hagworm.frame.gunicorn import DEFAULT_WORKER_STR, SIMPLE_LOG_CONFIG

# 进程数
workers = multiprocessing.cpu_count()

# 工人类
worker_class = DEFAULT_WORKER_STR

# 日志配置
logconfig_dict = SIMPLE_LOG_CONFIG
