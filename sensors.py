import board
from lib.adafruit_bme280 import basic as adafruit_bme280
from lib.adafruit_lsm6ds.lsm6dsox import LSM6DSOX
import lib.adafruit_lsm6ds as lsm6ds
from lib.adafruit_lis3mdl import LIS3MDL
import lib.adafruit_lis3mdl as lis3mdl
from debug import Debug

# Class to contain, manage, and access BME and SOX sensors
class Sensors:
    def __init__(self):
        self.test()
        self.precision = 2
    
    def configure(self, sea_level_pressure=1013.25):
        try:
            print("------ Configuring Sensors ------")
            
            Debug.timer_start()

            print("Configuring BME280...")
            self._bme280.sea_level_pressure = sea_level_pressure  # Set sea level pressure to 1013.25 hPa (standard value)
            
            print("Configuring LSM6DSOX...")
            self._sox.accelerometer_range = lsm6ds.AccelRange.RANGE_4G  # Set accelerometer range to +/- 4G
            self._sox.gyro_range = lsm6ds.GyroRange.RANGE_250_DPS  # Set gyro range to +/- 250 degrees per second
            self._sox.gyro_data_rate = lsm6ds.Rate.RATE_104_HZ  # Set gyro data rate to 104 Hz
            self._sox.accelerometer_data_rate = lsm6ds.Rate.RATE_104_HZ  # Set accelerometer data rate to 104 Hz
            
            print("Configuring LIS3MDL...")
            self._lis.range = lis3mdl.Range.RANGE_4_GAUSS  # Set magnetometer range to +/- 4 gauss
            self._lis.data_rate = lis3mdl.Rate.RATE_155_HZ  # Set magnetometer data rate to 155 Hz
            
            print("Sensors configured.")
            
            print()
            Debug.timer_stop("Configuring")

            print("---------------------------------")
            print()
        except Exception as e:
            print(f"Error configuring sensors: {e}")
    
    def test(self):
        print("-------- Testing Sensors --------")
        
        # Start the debug timer
        Debug.timer_start()
        
        # Set up working flags
        bme_working = False
        sox_working = False
        lis_working = False
        i2c_working = False
        
        # Test I2C
        print("Testing I2C...")
        try:
            # Set up I2C
            self._i2c = board.STEMMA_I2C()
            print("I2C is working.")
            i2c_working = True
        except Exception as e:
            print(f"I2C error: {e}")
        
        # Display the status of I2C
        Debug.status(i2c_working, (255, 255, 255))
        
        # Test BME280 sensor
        print("Testing BME280 sensor...")
        try:
            # Set up BME280 sensor
            self._bme280 = adafruit_bme280.Adafruit_BME280_I2C(self._i2c)
            self._bme280.pressure
            print("BME280 sensor is working.")
            bme_working = True
        except Exception as e:
            print(f"BME280 sensor error: {e}")
            
        # Diplay the status of BME280
        Debug.status(bme_working, (48, 116, 227))
        
        # Test LSM6DSOX sensor
        print("Testing LSM6DSOX sensor...")
        try:
            # Set up LSM6DSOX sensor
            self._sox = LSM6DSOX(self._i2c)
            self._sox.acceleration
            print("LSM6DSOX sensor is working.")
            sox_working = True
        except Exception as e:
            print(f"LSM6DSOX sensor error: {e}")
        
        # Display the status of LSM6DSOX
        Debug.status(sox_working, (227, 116, 48))
        
        # Test LIS3MDL sensor
        print("Testing LIS3MDL sensor...")
        try:
            # Set up LIS3MDL sensor
            self._lis = LIS3MDL(self._i2c)
            self._lis.magnetic
            print("LIS3MDL sensor is working.")
            lis_working = True
        except Exception as e:
            print(f"LIS3MDL sensor error: {e}")
        
        # Display the status of LIS3MDL
        Debug.status(lis_working, (194, 50, 227))
        
        # End the debug timer
        print()
        Debug.timer_stop("Testing")
        
        print("---------------------------------")
        print()

    @property
    def temperature(self) -> float:
        return self._bme280.temperature
    
    @property
    def pressure(self) -> float:
        return self._bme280.pressure
    
    @property
    def humidity(self) -> float:
        return self._bme280.humidity
    
    @property
    def altitude(self) -> float:
        return self._bme280.altitude
    
    @property
    def acceleration(self) -> tuple[float, float, float]:
        return self._sox.acceleration
    
    @property
    def gyro(self) -> tuple[float, float, float]:
        return self._sox.gyro
    
    @property
    def magnetic(self) -> tuple[float, float, float]:
        return self._lis.magnetic

    def _round(self, value :float, precision :int = 4):
        magnitude = pow(10, precision)
        value *= magnitude
        value = int(value)
        value = float(value) / magnitude
        return value