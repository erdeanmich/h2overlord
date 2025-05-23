
from bottle import route, run, Bottle, request, response
from schedule import Scheduler
from tinydb import TinyDB

from h2overlord_python.raspiservice import RaspiService, InterfaceRaspiService
from h2overlord_python.pumpservice import PumpService
from src.h2overlord_python.Config.config import Config

class Server: 
    server_router : PumpService
    bottle : Bottle = Bottle()

    def __init__(self, config: Config, raspi_service: InterfaceRaspiService, scheduler: Scheduler):
        self.server_router = PumpService(config, raspi_service, scheduler)
        self.config = config


    def start(self):
        print(f'Starting the server at h2overlord:8080')
        self.setup_routes()
        run(self.bottle, host='h2overlord', port=8080)

    def setup_routes(self):
        self.bottle.route('/status', 'GET', self.server_router.status)
        self.bottle.route('/schedule', 'POST', self.server_router.schedule)
        self.bottle.route('/action/pump-running', 'POST', self.server_router.toggle_pump_running)
        self.bottle.route('/action/pump-enable', 'POST', self.server_router.toggle_enable_pump)
        self.bottle.add_hook('after_request', self.enable_cors)

    def enable_cors(self):
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Access-Control-Allow-Methods'] = 'PUT, GET, POST, DELETE, OPTIONS'
        response.headers['Access-Control-Allow-Headers'] = 'Origin, Accept, Content-Type, X-Requested-With, X-CSRF-Token'
        