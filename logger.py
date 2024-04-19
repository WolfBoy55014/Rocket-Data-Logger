from lib import circuitpython_csv as csv
import os
import time

class Logger():
    def __init__(self, file_name :str) -> None:
        self.file_name = f"{file_name}.csv"
        self._create_file()
    
    def _create_file(self):
        # Check if .CSV file is already present. If not, we write CSV headers.
        all_files = os.listdir()  ## List all files in directory
        if self.file_name not in all_files:
            with open(self.file_name, mode="w", encoding="utf-8") as file:
                csv_writer = csv.writer(file)
                csv_writer.writerow(["Time", "Temperature", "Humidity", "Pressure", "Altitude", "Acceleration", "Gyro", "Magnetometer"])

    def log(self, temp, humidity, pressure, altitude, acceleration, gyro, magnetometer):
        with open(self.file_name, mode="a", encoding="utf-8") as file:
            csv_writer = csv.writer(file)
            csv_writer.writerow([time.monotonic(), temp, humidity, pressure, altitude, acceleration, gyro, magnetometer])