from lib import circuitpython_csv as csv
import os
import time
from debug import Debug

class Logger():
    def __init__(self, file_name :str) -> None:
        
        all_files = os.listdir("logs/")
        for n in range(10):
            # Check if a file with the current file name exists
            if f"{file_name}_{n}.csv" not in all_files:
                # If the file does not exist, set the current file name
                self.file_name = f"logs/{file_name}_{n}.csv"
                print(f"Writing to {self.file_name}")
                break
            # If the loop has reached 9, there are too many log files
            if n == 9:
                Debug.status(False, (255, 255, 0))
                raise Exception("Too many log files, remove old ones and try again")
            
        self._create_file()
    
    def _create_file(self):
        # Check if .CSV file is already present. If not, we write CSV headers.
        all_files = os.listdir()  # List all files in directory
        if self.file_name not in all_files:
            with open(self.file_name, mode="w", encoding="utf-8") as file:
                csv_writer = csv.writer(file)
                csv_writer.writerow(["Time", "Temperature", "Humidity", "Pressure", "Altitude", "Acceleration", "Gyro", "Magnetometer"])

    def log(self, temp, humidity, pressure, altitude, acceleration, gyro, magnetometer):
        with open(self.file_name, mode="a", encoding="utf-8") as file:
            csv_writer = csv.writer(file)
            csv_writer.writerow([time.monotonic(), temp, humidity, pressure, altitude, acceleration, gyro, magnetometer])