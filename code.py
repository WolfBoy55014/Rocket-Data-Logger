from sensors import Sensors
from logger import Logger
import supervisor

print(supervisor.runtime.usb_connected)

MODE = "LOG"
MODE = "LIVE"

sensors = Sensors()
sensors.configure()
log = Logger("log")

while True:
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
    