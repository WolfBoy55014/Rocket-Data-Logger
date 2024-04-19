import board
import storage
import digitalio
import time

# Set Up LED
led = digitalio.DigitalInOut(board.LED)
led.direction = digitalio.Direction.OUTPUT

storage.remount("/", False) # Make CIRCUITPY writable by computer if no sensors are attached

led.value = True
time.sleep(0.1)
led.value = False
time.sleep(0.1)
led.value = True
time.sleep(0.1)
led.value = False
time.sleep(0.1)