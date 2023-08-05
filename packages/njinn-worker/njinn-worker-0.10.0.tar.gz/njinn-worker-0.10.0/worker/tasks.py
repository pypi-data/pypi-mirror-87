import configparser
import json
import logging
import os
import shutil
import signal
import subprocess
import sys
import traceback
from datetime import datetime
from time import sleep

import requests
import virtualenv
from celery import exceptions
from celery.signals import after_setup_logger, after_setup_task_logger
from celery.utils.log import get_task_logger

# use absolute paths to be consistent & compatible bewteen worker code and the scripts
from worker.api_client import NjinnAPI
from worker.utils import is_windows
from worker.config import WorkerConfig, ActionExecutionConfig
from worker.celery_utils import get_celery_app


@after_setup_logger.connect
def setup_loggers(logger, *args, **kwargs):
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    # FileHandler
    fh = logging.FileHandler("logs.log")
    fh.setFormatter(formatter)
    logger.addHandler(fh)


@after_setup_task_logger.connect
def setup_task_loggers(logger, *args, **kwargs):
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    # FileHandler
    fh = logging.FileHandler("logs.log")
    fh.setFormatter(formatter)
    logger.addHandler(fh)


config = WorkerConfig().load_from_file().update_from_api()
app = get_celery_app(config.messaging_url)
log = get_task_logger(__name__)


@app.task(name="njinn_execute")
def njinn_execute(action, pack, action_context):
    global context
    proc = None
    working_dir = None
    try:

        abspath = os.path.abspath(__file__)
        dname = os.path.dirname(abspath)
        os.chdir(dname)

        dir_path = os.path.dirname(os.path.realpath(__file__))

        log.info("Njinn task initiating")

        action_execution_id = action_context.get("action_execution_id")
        working_dir = os.path.join("working", action_execution_id)
        log.debug("Creating working directory %s", working_dir)
        os.makedirs(working_dir)

        ActionExecutionConfig(
            working_dir,
            config_path=os.path.abspath(config.config_path),
            action=action,
            pack=pack,
            action_context=action_context,
        ).save()

        # Run detached, without a shell, and start a new group
        if is_windows():
            py_cmd = "python.exe"
        else:
            py_cmd = "python"

        cmd = [
            py_cmd,
            "action_task.py",
            f"{working_dir}",
        ]

        log.info("Running: %s", cmd)
        env = os.environ.copy()
        env["njinn_secrets_key"] = config.secrets_key
        proc = subprocess.Popen(cmd, cwd=dir_path, start_new_session=True, env=env)
        while os.path.exists(working_dir):
            sleep(0.1)
        log.info("Finished waiting")

    except exceptions.SoftTimeLimitExceeded:
        log.debug("Timeout")

        if proc:
            try:
                log.info("Trying to terminate child proces %s", proc.pid)
                proc.terminate()
            except Exception as e:
                log.warning("Problem terminating child process: %s", e)
        else:
            log.warning("No process found to terminate")

    return None
