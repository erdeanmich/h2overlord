import json
import logging
import re
import threading
import time
from pathlib import Path

import schedule
from schedule import Scheduler

from h2overlord_python.Config.config import Config
from h2overlord_python.raspiservice import RaspiService, MockRaspiService
from h2overlord_python.server import Server

def is_raspberry_pi() -> bool:
    """
    Return True when the program is running *on Raspberry-Pi hardware*.
    """
    # 1. The reliable modern way: read the Device-Tree model string
    model_file = Path("/sys/firmware/devicetree/base/model")
    try:
        # The file is NUL-terminated; strip both NUL and newline.
        model = model_file.read_bytes().decode().strip("\x00\n")
        if model.startswith("Raspberry Pi"):
            return True
    except FileNotFoundError:
        # Not a Linux with devicetree mounted (very old kernel or non-Linux OS)
        pass

    # 2. Fallback for very old kernels (< 4.7) : look at /proc/cpuinfo
    try:
        with open("/proc/cpuinfo", "r") as f:
            for line in f:
                if re.match(r"^Hardware\s*:\s*BCM", line):
                    return True  # classic Pi 1/2/3
                if "Raspberry Pi" in line:  # Pi 4 / CM4 expose the name here
                    return True
    except FileNotFoundError:
        pass

    # If none of the above matched we assume we are *not* on a Pi
    return False

def run_continuously(scheduler: Scheduler, interval=1):
    """Continuously run, while executing pending jobs at each
    elapsed time interval.
    @return cease_continuous_run: threading. Event which can
    be set to cease continuous run. Please note that it is
    *intended behavior that run_continuously() does not run
    missed jobs*. For example, if you've registered a job that
    should run every minute and you set a continuous run
    interval of one hour then your job won't be run 60 times
    at each interval but only once.
    """
    cease_continuous_run = threading.Event()

    class ScheduleThread(threading.Thread):
        @classmethod
        def run(cls):
            while not cease_continuous_run.is_set():
                logging.getLogger().debug('Run scheduler tick!')
                scheduler.run_pending()
                time.sleep(interval)

    continuous_thread = ScheduleThread()
    continuous_thread.start()
    return cease_continuous_run

if __name__ == '__main__':
    logging.basicConfig(filename='debug.log', level=logging.DEBUG)
    logging.getLogger().debug('Starting the H2Overlord backend!')
    config = Config(**json.loads(open('./Config/config.json').read()))
    logging.getLogger().debug(config)
    scheduler = schedule.Scheduler()
    background_task = run_continuously(scheduler,30)

    if is_raspberry_pi():
        raspi_service = RaspiService(config)
    else:
        raspi_service = MockRaspiService()

    server = Server(config, raspi_service, scheduler)
    server.start()
    


