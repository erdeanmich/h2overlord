import json
import re

import pendulum
import schedule
from bottle import request, abort, response
from schedule import Scheduler
from tinydb import TinyDB
from tinydb.table import Document

from h2overlord_python.Config.config import Config
from h2overlord_python.Data.pumpstate import PumpState
from h2overlord_python.raspiservice import InterfaceRaspiService


class PumpService:
    config: Config
    raspi_service: InterfaceRaspiService
    pump_state: PumpState
    scheduler: Scheduler
    db: TinyDB = TinyDB('state.json')

    def __init__(self, config: Config, raspi_service: InterfaceRaspiService, scheduler : Scheduler):
        self.config = config
        self.raspi_service = raspi_service
        self.pump_state = PumpState(
            False, False, self.raspi_service.get_temperature(), self.raspi_service.get_humidity(), '', 0
        )
        if len(self.db.all()) == 0:
            self.dump_state_to_db()
        else:
            self.fetch_state_from_db()

        print(self.pump_state)
        self.scheduler = scheduler
        self.initialize_scheduler()

    def fetch_state_from_db(self):
        db_state = self.db.get(doc_id=1)
        self.pump_state.isEnabled = db_state['isEnabled']
        self.pump_state.isRunning = db_state['isRunning']
        self.pump_state.temperature = db_state['temperature']
        self.pump_state.humidity = db_state['humidity']
        self.pump_state.currentDuration = db_state['currentDuration']
        self.pump_state.currentSchedule = db_state['currentSchedule']

    def dump_state_to_db(self):
        self.db.upsert(Document(self.pump_state.__dict__, doc_id=1))

    def status(self):
        print("Returning Status!")
        response.content_type='application/json'
        self.fetch_state_from_db()
        self.pump_state.temperature = self.raspi_service.get_temperature()
        self.pump_state.humidity = self.raspi_service.get_humidity()
        self.dump_state_to_db()
        return json.dumps(self.pump_state.__dict__)

    def schedule(self):
        self.fetch_state_from_db()
        time: str = request.json['time']
        duration: int = request.json['duration']

        if not self.validate_time(time):
            abort(500, "Invalid time")
            return

        self.pump_state.currentSchedule = time
        self.pump_state.currentDuration = duration

        schedule.clear()
        
        if time == '' or duration == 0:
            self.dump_state_to_db()
            return self.status()

        self.initialize_scheduler()
        self.dump_state_to_db()
        return self.status()

    def initialize_scheduler(self):
        if self.pump_state.currentSchedule == '' or self.pump_state.currentDuration == 0:
            return 
        
        dt = pendulum.parse(self.pump_state.currentSchedule)
        self.scheduler.every().day.at(dt.to_time_string()).do(self.schedule_pump(True))
        dt = dt.add(minutes=self.pump_state.currentDuration)
        self.scheduler.every().day.at(dt.to_time_string()).do(self.schedule_pump(False))

    def toggle_pump_running(self):
        self.fetch_state_from_db()
        if self.pump_state.isEnabled:
            self.raspi_service.toggle_pump_relay()
            self.pump_state.isRunning = not self.pump_state.isRunning
            self.dump_state_to_db()

        return self.status()

    def toggle_enable_pump(self):
        self.fetch_state_from_db()
        self.pump_state.isEnabled = not self.pump_state.isEnabled
        self.dump_state_to_db()
        return self.status()

    def validate_time(self, time: str):
        if time == '':
            return True
        
        pattern = re.compile(r"\d\d:\d\d", re.IGNORECASE)
        return pattern.match(time)

    def schedule_pump(self, pump_active: bool):
        active = self.pump_state.isEnabled and pump_active
        self.pump_state.isRunning = active
        self.raspi_service.set_pump_relay(active)
