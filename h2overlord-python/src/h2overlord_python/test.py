from time import sleep

import gpiozero

RELAY_PIN = 16
RELAY = None

def toggle_pump_relay():
    RELAY.toggle()
    print(f'Relay status is: {RELAY.value}')


if __name__ == '__main__':
    RELAY = gpiozero.OutputDevice(RELAY_PIN)
    print('Starting the test script!')
    while True:
        sleep(2)
        toggle_pump_relay()
