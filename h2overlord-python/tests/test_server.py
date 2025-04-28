import unittest
from unittest.mock import MagicMock

from schedule import Scheduler

from h2overlord_python.Config.config import Config
from h2overlord_python.raspiservice import RaspiService
from h2overlord_python.server import Server


class MyTestCase(unittest.TestCase):
    server_pid = None
    server: Server = None
    raspi_handler : RaspiService = None
    config: Config = None
    scheduler : Scheduler = None
    
    def setUp(self):
        self.raspi_handler = MagicMock()
        self.config = MagicMock()
        self.scheduler = MagicMock()
        self.server = Server(self.config, self.raspi_handler, self.scheduler)
        self.config.baseUrl = '/h2overlord/'
    
    def test_initial_state(self):
        self.server.start()
    
if __name__ == '__main__':
    unittest.main()
