import logging
import os
from logging.config import dictConfig
import threading
import uuid
import sys
from io import StringIO
from pathlib import PurePath
from typing import Dict, Union, Tuple, List

import narration
import pendulum

from constellate.logger.logmode import LogMode
from constellate.logger.loggers import Loggers
from constellate.logger.stringhandler import StringHandler


class _LogDefault:
    LOGS_DIRECTORY = os.getcwd()
    ROOT_LOGGER_NAME = "default"
    MODE = LogMode = (
        LogMode.ENV_PRODUCTION
        | LogMode.INTERACTIVE_NO
        | LogMode.DETAIL_NORMAL
        | LogMode.OPERATE_STANDALONE
    )


class Log(object):
    _LOGGER_NAMES_RETRIEVED = {}
    # Logger instance are held by python sdk private dictionary. Only loggers names are tracked
    _LOGGER_NAMES_EXTERNAL = set()
    _HANDLERS_CACHE = {}
    _JOB_LOGGER_NAMES_LOCK = threading.Lock()
    _LOGS_DIRECTORY = _LogDefault.LOGS_DIRECTORY
    _ROOT_LOGGER_NAME = _LogDefault.ROOT_LOGGER_NAME

    def default_config_dict(root_name=None, mode: LogMode = _LogDefault.MODE):
        COLOR_MARKER = "%(log_color)s"

        def console_formatter(name=None, mode=None, normal_fmt=None, trace_fmt=None):
            remove_color = mode not in LogMode.INTERACTIVE_YES
            fmt = trace_fmt if mode in LogMode.DETAIL_TRACE else normal_fmt
            fmt = fmt.replace(COLOR_MARKER, "") if remove_color else fmt
            colored = "colored" if not remove_color else "monocolor"
            key = f"console_{colored}_{name}"
            return (
                key,
                {
                    key: {
                        "class": "logging.Formatter"
                        if remove_color
                        else "colorlog.ColoredFormatter",
                        "format": fmt,
                        "date_fmt": "%Y-%m-%d %H:%M:%S",
                    }
                },
            )

        def file_formatter(name=None, mode=None, normal_fmt=None, trace_fmt=None):
            key = f"fmt_{name}"
            fmt = trace_fmt if mode in LogMode.DETAIL_TRACE else normal_fmt
            return (key, {key: {"class": "logging.Formatter", "format": fmt}})

        def rotating_file_handler(name=None, fmt_id=None, filename=None) -> Tuple[str, Dict]:
            key = f"rfhd_{name}"
            return (
                key,
                {
                    key: {
                        "class": "logging.handlers.TimedRotatingFileHandler",
                        "filename": filename,
                        "when": "W0",
                        "backupCount": 4,
                        "encoding": "utf-8",
                        "delay": False,
                        "utc": True,
                        "atTime": pendulum.time(23, 59, 0, 0),
                        "formatter": fmt_id,
                    }
                },
            )

        def console_handler(name=None, formatter=None) -> Tuple[str, Dict]:
            key = f"console_{name}"
            return (
                key,
                {
                    key: {
                        "class": "logging.StreamHandler",
                        "formatter": formatter,
                        "stream": sys.stdout,
                    }
                },
            )

        def logger(
            name=None,
            handlers=[],
            levelIFProd="INFO",
            mode=None,
            levelIfNotProd="DEBUG",
            propagate=False,
        ):
            return {
                f"{name}": {
                    "handlers": handlers,
                    "level": levelIFProd if mode in LogMode.ENV_PRODUCTION else levelIfNotProd,
                    "propagate": propagate,
                }
            }

        console_fmt_id, console_fmt = console_formatter(
            name="console",
            mode=mode,
            normal_fmt=f"%(asctime)s: P%(process)d: %(processName)s: T%(thread)d: %(threadName)s: {COLOR_MARKER}%(levelname)s: %(message)s",
            trace_fmt=f"%(asctime)s: P%(process)d: %(processName)s: T%(thread)d: %(threadName)s: %(name)s: {COLOR_MARKER}%(levelname)s: %(message)s",
        )
        file_fmt_id, file_fmt = file_formatter(
            name="detailed",
            mode=mode,
            normal_fmt="%(asctime)s: P%(process)d: %(processName)s: T%(thread)d: %(threadName)s: %(levelname)s: %(message)s",
            trace_fmt="%(asctime)s: P%(process)d: %(processName)s: T%(thread)d: %(threadName)s: %(levelname)s: %(message)s",
        )
        root_file_fmt_id, root_file_fmt = file_formatter(
            name="root_detailed",
            mode=mode,
            normal_fmt="%(asctime)s: P%(process)d: %(processName)s: T%(thread)d: %(threadName)s: %(levelname)s: %(message)s",
            trace_fmt="%(asctime)s: P%(process)d: %(processName)s: T%(thread)d: %(threadName)s: %(name)s: %(levelname)s: %(message)s",
        )

        console_hd_id, console_hd = console_handler(name=f"{root_name}", formatter=console_fmt_id)
        root_fhd_id, root_fhd = rotating_file_handler(
            name=f"{root_name}",
            fmt_id=file_fmt_id,
            filename=f"{Log._LOGS_DIRECTORY}/{root_name}.log",
        )
        root_app_fhd_id, root_app_fhd = rotating_file_handler(
            name=f"{root_name}.app",
            fmt_id=file_fmt_id,
            filename=f"{Log._LOGS_DIRECTORY}/{root_name}.app.log",
        )
        root_network_fhd_id, root_network_fhd = rotating_file_handler(
            name=f"{root_name}.network",
            fmt_id=file_fmt_id,
            filename=f"{Log._LOGS_DIRECTORY}/{root_name}.network.log",
        )
        root_database_fhd_id, root_database_fhd = rotating_file_handler(
            name=f"{root_name}.database",
            fmt_id=file_fmt_id,
            filename=f"{Log._LOGS_DIRECTORY}/{root_name}.database.log",
        )
        root_media_fhd_id, root_media_fhd = rotating_file_handler(
            name=f"{root_name}.media",
            fmt_id=file_fmt_id,
            filename=f"{Log._LOGS_DIRECTORY}/{root_name}.media.log",
        )
        config = {
            "disable_existing_loggers": False,
            "version": 1,
            "formatters": {
                **console_fmt,
                **file_fmt,
                **root_file_fmt,
            },
            "handlers": {
                **console_hd,
                **root_fhd,
                **root_app_fhd,
                **root_network_fhd,
                **root_database_fhd,
                **root_media_fhd,
            },
            "loggers": {
                **logger(
                    name=f"{root_name}",
                    handlers=[console_hd_id, root_fhd_id],
                    levelIfNotProd="DEBUG",
                    mode=mode,
                    levelIFProd="WARN",
                    propagate=False,
                ),
                **logger(
                    name=f"{root_name}.app",
                    handlers=[root_app_fhd_id],
                    levelIfNotProd="DEBUG",
                    mode=mode,
                    levelIFProd="WARN",
                    propagate=True,
                ),
                **logger(
                    name=f"{root_name}.network",
                    handlers=[root_network_fhd_id],
                    levelIfNotProd="DEBUG",
                    mode=mode,
                    levelIFProd="WARN",
                    propagate=True,
                ),
                **logger(
                    name=f"{root_name}.database",
                    handlers=[root_database_fhd_id],
                    levelIfNotProd="DEBUG",
                    mode=mode,
                    levelIFProd="WARN",
                    propagate=True,
                ),
                **logger(
                    name=f"{root_name}.media",
                    handlers=[root_media_fhd_id],
                    levelIfNotProd="DEBUG",
                    mode=mode,
                    levelIFProd="WARN",
                    propagate=True,
                ),
            },
        }
        return config

    @staticmethod
    def setup(
        root_logger_name: str = _LogDefault.ROOT_LOGGER_NAME,
        log_dir_path: str = _LogDefault.LOGS_DIRECTORY,
        mode: LogMode = _LogDefault.MODE,
        config_dict: Dict = None,
    ):
        Log._LOGS_DIRECTORY = log_dir_path
        Log._ROOT_LOGGER_NAME = root_logger_name

        # Load default logger config dict
        if config_dict is None:
            config_dict = Log.default_config_dict(root_name=Log._ROOT_LOGGER_NAME, mode=mode)

        # Load declarative config
        try:
            dictConfig(config_dict)
        except BaseException as e:
            print(f"ERROR: Cannot configure loggers: {e}")
            raise

        # Keep track of loggers being setup
        logger_names = list(config_dict.get("loggers", {}).keys())
        for name in logger_names:
            Log._LOGGER_NAMES_EXTERNAL.add(name)

    @staticmethod
    def get_file_path(fileName=None):
        return (
            PurePath(Log._LOGS_DIRECTORY, fileName)
            if Log._LOGS_DIRECTORY is not None
            else PurePath(fileName)
        )

    @staticmethod
    def shutdown_all_loggers():
        # Fixme teardown wrapper logger handlers narration.teardown_loggers
        logging.shutdown()

    @staticmethod
    def get_native_logger(name=None) -> Tuple[bool, logging.Logger]:
        """
        @return A logger instance and whether it existed before
        """
        exist = Log._LOGGER_NAMES_RETRIEVED.get(name, False)
        if not exist:
            Log._LOGGER_NAMES_RETRIEVED[name] = True
        return exist, logging.getLogger(name)

    @staticmethod
    def get_hierarchical_logger(
        root=None,
        prefix=None,
        suffix=None,
        mode: LogMode = LogMode.OPERATE_SERVER,
        mode_settings: Dict = {},
    ):
        """
        @return A logger instance
        """
        # Construct Fully Qualified Logger Name
        io = StringIO()
        if root is not None:
            io.write(root)
        if prefix is not None:
            io.write(f".{prefix}")
        if suffix is not None:
            io.write(f".{suffix}")

        name = io.getvalue()

        existed, logger = Log.get_native_logger(name=name)
        if not existed:
            # Client mode logger should not have any handlers set by default, as it will create as many handlers as
            # the original "server" logger had
            if mode in LogMode.OPERATE_CLIENT:
                for i, handler in enumerate(logger.handlers):
                    logger.removeHandler(handler)

        # Decide whether to propagate to upper logger
        if mode in LogMode.OPERATE_SERVER:
            # Propagate log to ancestor loggers.
            logger.propagate = True
        elif mode in LogMode.OPERATE_CLIENT:
            # Client logger's handlers must not propagate. The server's logger
            # handlers will do so if configured
            logger.propagate = False
        elif mode in LogMode.OPERATE_STANDALONE:
            # Let initial loggers configuration decide
            pass

        # Gather log records into main process's logging thread for that logger
        # Other (forked) processed will simply send log records to the main process
        if mode in LogMode.OPERATE_SERVER:
            ctx = mode_settings["ctx"]
            ctx_manager = mode_settings["ctx_manager"]
            client_handler_settings = narration.setup_server_handlers(
                logger=logger, ctx=ctx, ctx_manager=ctx_manager
            )
            return logger, client_handler_settings
        elif mode in LogMode.OPERATE_CLIENT:
            narration.setup_client_handlers(
                logger=logger, handler_name_to_client_handler_settings=mode_settings
            )
            return logger, {}
        elif mode in LogMode.OPERATE_STANDALONE:
            return logger, {}

    @staticmethod
    def create_job_handler(capacity=sys.maxsize):
        """
        @return In-Memory Handler instance
        """
        handler = StringHandler(capacity=capacity)
        formatter = logging.Formatter("%(message)s")
        handler.setFormatter(formatter)
        return handler

    @staticmethod
    def get_available_job_logger(level=logging.DEBUG, capacity=sys.maxsize, console=False):
        """
        @return Create or get a free Job logger instance
        """
        with Log._JOB_LOGGER_NAMES_LOCK:
            defaultHandlers = [Log._CONSOLE_HANDLER] if console else []

            handler = Log.create_job_handler(capacity=capacity)
            logger = logging.getLogger(name=str(uuid.uuid4()))
            logger.setLevel(level)

            for defaultHandler in [handler] + defaultHandlers:
                logger.addHandler(defaultHandler)
            return logger

    @staticmethod
    def free_job_logger(logger=None):
        """
        @return Create or get a free Job logger instance
        """
        with Log._JOB_LOGGER_NAMES_LOCK:
            if logger is not None:
                # Note: This is a private controller, at least available on Python 3.7
                name = logger.name
                loggers = logging.Logger.manager.loggerDict
                if name in loggers:
                    del loggers[logger.name]
                if name in Log._LOGGER_NAMES_RETRIEVED:
                    del Log._LOGGER_NAMES_RETRIEVED[name]

    @staticmethod
    def loggers(
        mode: LogMode = LogMode.OPERATE_SERVER,
        mode_settings: Union[Dict, Loggers] = None,
        logger_names: List[str] = None,
    ) -> Loggers:
        """
        mode_settings: Settings vary per LoggerMode.

        LoggerMode.SERVER's settings are:
        {
            ctx: mp.get_context(...),
            ctx_manager: ctx.Manager()
        }

        LoggerMode.CLIENT's settings be: Loggers.setting()
        """

        def get_logger_short_name(parts_count, prefix, suffix):
            name = (
                "root"
                if parts_count == 1
                else prefix
                if parts_count == 2
                else f"{prefix}_{suffix}"
                if parts_count > 2
                else None
            )
            return name

        def get_settings(short_name, mode_settings):
            if isinstance(mode_settings, Loggers):
                return mode_settings._get_settings(short_name)
            return mode_settings

        loggers = Loggers()

        # Logger instance already exists (due to setup). Retrieve them only,
        # albeit with modification
        logger_names = logger_names if logger_names is not None else Log._LOGGER_NAMES_EXTERNAL
        for logger_name in logger_names:

            parts = logger_name.split(".")
            parts_count = len(parts)

            root = parts[0]
            prefix = parts[1] if parts_count > 1 else None
            suffix = parts[2] if parts_count > 2 else None

            assert parts_count < 3, "not handling case where logger name is 3+ parts"

            short_name = get_logger_short_name(parts_count, prefix, suffix)
            mode_settings = get_settings(short_name, mode_settings)
            logger, client_logger_settings = Log.get_hierarchical_logger(
                root=root, prefix=prefix, suffix=suffix, mode=mode, mode_settings=mode_settings
            )
            loggers.populate_with(name=short_name, logger=logger, settings=client_logger_settings)

        return loggers
