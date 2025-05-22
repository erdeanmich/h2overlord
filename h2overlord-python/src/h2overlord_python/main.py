import json
import threading
import time

import schedule

from h2overlord_python.Config.config import Config
from h2overlord_python.raspiservice import RaspiService
from h2overlord_python.server import Server

def run_continuously(interval=1):
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
                schedule.run_pending()
                time.sleep(interval)
                print("Scheduler tick")

    continuous_thread = ScheduleThread()
    continuous_thread.start()
    return cease_continuous_run

if __name__ == '__main__':
    print('Starting the H2Overlord backend!')
    config = Config(**json.loads(open('./Config/config.json').read()))
    print(config)
    background_task = run_continuously(60)
    server = Server(config, None, schedule.Scheduler())
    server.start()
    


