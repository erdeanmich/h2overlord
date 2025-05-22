from dataclasses import dataclass

@dataclass 
class Config: 
    baseUrl: str
    relayGpioPin: int
    bme280GpioPin: int    
    