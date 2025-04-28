import bme280
import gpiozero
import smbus2
from gpiozero import OutputDevice
from smbus2.smbus2 import SMBus
from h2overlord_python.Config.config import Config

class RaspiService:
    relay: OutputDevice = None
    bme280_params = None
    smbus: SMBus = None
    address = 0x76
    
    def __init__(self, config: Config):
        self.config = config
        self.relay = gpiozero.OutputDevice(config.relayGpioPin, active_high=False)
        self.smbus = smbus2.SMBus(1)
        self.bme280_params = bme280.load_calibration_params(self.smbus, self.address)
        
    def toggle_pump_relay(self):
        self.relay.toggle()
        
    def set_pump_relay(self, active: bool):
        if active:
            self.relay.on()
        else:
            self.relay.off()
            
    def get_temperature(self):
        data = self.read_bme280_data()
        return data.temperature
    
    def get_humidity(self):
        data = self.read_bme280_data()
        return data.humidity
    
    def read_bme280_data(self):
        return bme280.sample(self.smbus, self.address, self.bme280_params)
        