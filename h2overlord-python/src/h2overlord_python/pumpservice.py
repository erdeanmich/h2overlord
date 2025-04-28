import json
import re

import pendulum
import schedule
from bottle import request, abort
from schedule import Scheduler

from h2overlord_python.Config.config import Config
from h2overlord_python.Data.pumpstate import PumpState
from h2overlord_python.raspiservice import RaspiService


class PumpService:
    config: Config
    raspi_service: RaspiService
    pump_state: PumpState
    scheduler: Scheduler

    def __init__(self, config: Config, raspi_handler: RaspiService, scheduler : Scheduler):
        self.config = config
        self.raspi_service = raspi_handler
        self.pump_state = PumpState(False, False, 0, 0, '', 0)
        self.scheduler = scheduler

    def status(self):
        return json.dumps(self.pump_state.__dict__)

    def schedule(self):
        print(request.json)
        time: str = request.json['time']
        duration: int = request.json['duration']

        if not self.validate_time(time):
            abort(500, "Invalid time")
            return

        self.pump_state.currentSchedule = time
        self.pump_state.currentDuration = duration

        schedule.clear()
        dt = pendulum.parse(time)
        self.scheduler.every().day.at(dt.to_time_string()).do(self.schedule_pump(True))

        dt = dt.add(minutes=duration)
        self.scheduler.every().day.at(dt.to_time_string()).do(self.schedule_pump(False))

        return self.status()

    def toggle_pump_running(self):
        if self.pump_state.isEnabled:
            self.raspi_service.toggle_pump_relay()
            self.pump_state.isRunning = not self.pump_state.isRunning

        return self.status()

    def toggle_enable_pump(self):
        self.pump_state.isEnabled = not self.pump_state.isEnabled
        return self.status()

    def validate_time(self, time: str):
        pattern = re.compile(r"\d\d:\d\d", re.IGNORECASE)
        return pattern.match(time)

    def schedule_pump(self, pump_active: bool):
        active = self.pump_state.isEnabled and pump_active
        self.pump_state.isRunning = active
        self.raspi_service.set_pump_relay(active)
