# -*- coding: utf-8 -*-

import fastapi

from fastapi import __version__ as fastapi_version

from hagworm import hagworm_label, hagworm_slogan
from hagworm import __version__ as hagworm_version
from hagworm.extend.asyncio.base import Utils
from hagworm.extend.logging import DEFAULT_LOG_FILE_ROTATOR, DEFAULT_LOG_INTERCEPTOR, init_logger


DEFAULT_HEADERS = [(r'Server', hagworm_label)]


def create_fastapi(
        log_level=r'info', log_handler=DEFAULT_LOG_INTERCEPTOR, log_file_path=None,
        log_file_rotation=DEFAULT_LOG_FILE_ROTATOR, log_file_retention=0xff,
        debug=False,
        **setting
):

    init_logger(
        log_level.upper(),
        log_handler,
        log_file_path,
        log_file_rotation,
        log_file_retention,
        debug
    )

    environment = Utils.environment()

    Utils.log.info(
        f'{hagworm_slogan}'
        f'hagworm {hagworm_version}\n'
        f'fastapi {fastapi_version}\n'
        f'python {environment["python"]}\n'
        f'system {" ".join(environment["system"])}'
    )

    setting.setdefault(r'debug', debug)
    setting.setdefault(r'title', r'Hagworm')
    setting.setdefault(r'version', hagworm_version)

    return fastapi.FastAPI(**setting)
