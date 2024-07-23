import board
import storage
import digitalio
import time
import os
import sdcardio

# Set Up LED
led = digitalio.DigitalInOut(board.LED)
led.direction = digitalio.Direction.OUTPUT

# spi = board.SPI()
# cs = board.D25     # Use the pin you wired to the breakout CS
# 
# sdcard = sdcardio.SDCard(spi, cs)
# vfs = storage.VfsFat(sdcard)
# storage.mount(vfs, "/sd")

if os.getenv("OUTPUT_MODE") == "LOG":
    storage.remount("/", False) # Make CIRCUITPY writable by computer if no sensors are attached

    led.value = True
    time.sleep(0.1)
    led.value = False
    time.sleep(0.1)
    led.value = True
    time.sleep(0.1)
    led.value = False
    time.sleep(0.1)