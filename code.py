from sensors import Sensors
from logger import Logger
import supervisor
from debug import Debug
import digitalio
import board
from time import sleep
import os

# Check if the board was soft-reset
if supervisor.runtime.run_reason == supervisor.RunReason.SUPERVISOR_RELOAD:
    import microcontroller
    
    # If it was, reboot into safe mode (to prevent corruption on power off)
    microcontroller.on_next_reset(microcontroller.RunMode.SAFE_MODE)
    microcontroller.reset()

MODE = os.getenv("OUTPUT_MODE")
MIN_RAM_BEFORE_CLEAR = int(os.getenv("MIN_RAM_BEFORE_CLEAR"))
DISABLE_GC = os.getenv("DISABLE_GC", "FALSE") == "TRUE"
if DISABLE_GC:
    import gc
    gc.disable()

# Init sensors
sensors = Sensors()
sensors.configure()

# Init logging
if MODE == "LOG":
    log = Logger("log")

# Config Shutdown button (BOOTSEL)
shutdown_pin = digitalio.DigitalInOut(board.BUTTON)
shutdown_pin.direction = digitalio.Direction.INPUT
shutdown_pin.pull = digitalio.Pull.UP

while True:
    
    # Pseudo-auto GC
    if DISABLE_GC and gc.mem_free() < MIN_RAM_BEFORE_CLEAR:
        gc.collect()
        
    # Detect if shutdown has been pressed
    if not shutdown_pin.value:
        Debug.led_on()
        sleep(0.7)
        Debug.led_off()
        sleep(0.2)
        Debug.led_on()
        sleep(0.1)
        Debug.led_off()
        
        supervisor.reload()
    
    pressure = 0
    temperature = 0
    humidity = 0
    altitude = 0
    accel = (0, 0, 0)
    gyro = (0, 0, 0)
    magnet = (0, 0, 0)
    
    # Get Atmospheric data
    try:
        pressure = sensors.pressure
        temperature = sensors.temperature
        humidity = sensors.humidity
        altitude = sensors.altitude
    except Exception as e:
        print(f"BME280 Error {e}, continuing...")
    
    # Get Accelerometer/Gyro data
    try:
        accel = sensors.acceleration
        gyro = sensors.gyro
    except Exception as e:
        print(f"LSM6DSOX Error {e}, continuing...")
        
    # Get Magnetometer data
    try:
        magnet = sensors.magnetic
    except Exception as e:
        print(f"LIS3MDL Error {e}, continuing...")
    
    if MODE is "LOG":
        log.log(temperature, humidity, pressure, altitude, accel, gyro, magnet) # About 3.17 hours of data can be stored on the flash
    elif MODE is "LIVE":
        print(f"Pressure: {pressure:.2f} Temp: {temperature:.2f} Humidity: {humidity:.2f} Altitude: {altitude:.2f} Accel: ({accel[0]:.2f}, {accel[1]:.2f}, {accel[2]:.2f}) Gyro: ({gyro[0]:.2f}, {gyro[1]:.2f}, {gyro[2]:.2f}) Magnet: ({magnet[0]:.2f}, {magnet[1]:.2f}, {magnet[2]:.2f})")
    
    Debug.toggle_led()