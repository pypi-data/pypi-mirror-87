import configparser
import os
import sys

import click

# use absolute paths to be consistent & compatible bewteen worker code and the scripts
from worker.config import WorkerConfig, get_config_path
from worker.njinnworker import NjinnWorker


@click.command()
@click.option("-a", "--api", "api", help="Njinn API url.")
@click.argument("token", required=False)
def main(api=None, token=None):
    # windows celery fix: https://github.com/celery/celery/issues/4081
    os.environ["FORKED_BY_MULTIPROCESSING"] = "1"
    os.environ["GIT_TERMINAL_PROMPT"] = "0"

    njinn_url = sys.argv[-2] if len(sys.argv) > 2 else os.getenv("NJINN_URL")
    registration_token = token or os.getenv("NJINN_WORKER_TOKEN")
    print("Config file:", get_config_path())
    worker = NjinnWorker(registration_token=registration_token, njinn_url=njinn_url)
    print("Working Directory:", worker.working_dir)
    worker.start()


if __name__ == "__main__":
    main()
