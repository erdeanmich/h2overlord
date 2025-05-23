
import bme280
import gpiozero
import smbus2
from bme280 import compensated_readings
from gpiozero import OutputDevice
import RPi.GPIO as GPIO
from smbus2.smbus2 import SMBus
from h2overlord_python.Config.config import Config

class InterfaceRaspiService:
    def toggle_pump_relay(self):
        pass

    def set_pump_relay(self, active: bool):
        pass

    def get_temperature(self) -> float:
        pass

    def get_humidity(self) -> float:
        pass


class RaspiService(InterfaceRaspiService):
    relay: OutputDevice = None
    bme280_params = None
    smbus: SMBus = None
    address = 0x76

    def __init__(self, config: Config):
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
            
    def get_temperature(self) -> float:
        data = self.read_bme280_data()
        return data.temperature
    
    def get_humidity(self) -> float:
        data = self.read_bme280_data()
        return data.humidity
    
    def read_bme280_data(self) -> compensated_readings:
        return bme280.sample(self.smbus, self.address, self.bme280_params)


class MockRaspiService(InterfaceRaspiService):

    def __init__(self):
        print('Not on Raspberry Pi! Using the mock service!')

    def toggle_pump_relay(self):
        print('Mock toggle relay')

    def set_pump_relay(self, active: bool):
        print('Mock set pump relay')

    def get_temperature(self) -> float:
        return 20

    def get_humidity(self) -> float:
        return 0.5
