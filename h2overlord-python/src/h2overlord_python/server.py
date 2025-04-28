import json
from wsgiref.simple_server import server_version

from bottle import route, run, Bottle, request
from numpy.ma.core import append, flatten_structured_array
from schedule import Scheduler

from h2overlord_python.Data.pumpstate import PumpState
from h2overlord_python.raspiservice import RaspiService
from h2overlord_python.pumpservice import PumpService
from src.h2overlord_python.Config.config import Config

class Server: 
    server_router : PumpService
    main_server : Bottle = Bottle()
    bottle : Bottle = Bottle()

    def __init__(self, config: Config, raspi_handler: RaspiService, scheduler: Scheduler):
        self.server_router = PumpService(config, raspi_handler, scheduler)
        self.config = config

    def start(self):
        print(f'Starting the server at base url {self.config.baseUrl}')
        self.setup_routes()
        self.main_server.mount(self.config.baseUrl, self.bottle)
        run(self.main_server, host='localhost', port=8080)

    def setup_routes(self):
        self.bottle.route('/status', 'GET', self.server_router.status)
        self.bottle.route('/schedule', 'POST', self.server_router.schedule)
        self.bottle.route('/action/pump-running', 'POST', self.server_router.toggle_pump_running)
        self.bottle.route('/action/pump-enable', 'POST', self.server_router.toggle_enable_pump)
    
        