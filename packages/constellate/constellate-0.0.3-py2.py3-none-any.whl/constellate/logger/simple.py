import multiprocessing
from typing import Dict

from constellate.logger.log import Log
from constellate.logger.logmode import LogMode
from constellate.logger.loggers import Loggers


def setup_any_process_loggers(
    root_logger_name="unnamped", log_dir_path=None, mode=None, config_dict: Dict = None
):
    """
    Setup constant applying to all loggers
    """
    Log.setup(
        root_logger_name=root_logger_name,
        log_dir_path=log_dir_path,
        mode=mode,
        config_dict=config_dict,
    )


def setup_standalone_process_loggers() -> Loggers:
    """
    Setup loggers for an app (no logging to be shared with child processes , if any)
    """
    mode_settings = {}
    return Log.loggers(mode=LogMode.OPERATE_STANDALONE, mode_settings=mode_settings)


def setup_main_process_loggers(ctx=multiprocessing.get_context()) -> Loggers:
    """
    Setup loggers in "server mode" for an app's main process
    """
    mode_settings = {"ctx": ctx, "ctx_manager": ctx.Manager()}
    return Log.loggers(mode=LogMode.OPERATE_SERVER, mode_settings=mode_settings)


def setup_child_process_loggers(mode_settings: Loggers = None) -> Loggers:
    """
    Setup loggers in "client" mode for an app's child process (ie forked, spawn, etc)
    """
    return Log.loggers(mode=LogMode.OPERATE_CLIENT, mode_settings=mode_settings)


def teardown_loggers():
    "Free/Remove all loggers setup previously"
    Log.shutdown_all_loggers()
