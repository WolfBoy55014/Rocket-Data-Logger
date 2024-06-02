from lib import circuitpython_csv as csv
import os
import time
from debug import Debug
import gc

MAX_LOGS = os.getenv(
    "MAX_LOGS"
)  # Get the maximum number of log files from the environment variables

LOG_DIR = os.getenv("LOG_DIR")  # Get the file directory from the environment variables

LOG_BUFFER_LENGTH = os.getenv(
    "LOG_BUFFER_LENGTH"
)  # Get the log buffer length from the environment variables

MIN_RAM_BEFORE_CLEAR = os.getenv(
    "MIN_RAM_BEFORE_CLEAR"
)  # Get the minimum amount of RAM before clearing the log buffer from the environment variables

class Logger:
    def __init__(self, file_name: str) -> None:

        self.buffer = []

        all_files = os.listdir(LOG_DIR)  # Get all files in the log directory
        for n in range(MAX_LOGS):
            # Check if a file with the current file name exists
            if f"{file_name}_{n}.csv" not in all_files:
                # If the file does not exist, set the current file name
                self.file_name = f"{LOG_DIR}{file_name}_{n}.csv"
                print(f"Writing to {self.file_name}")
                break
            # If the loop has reached 9, there are too many log files
            if n == MAX_LOGS - 1:
                Debug.status(False, (255, 255, 0))
                raise Exception("Too many log files, remove old ones and try again")

        self._create_file()

    def _create_file(self):
        # Check if .CSV file is already present. If not, we write CSV headers.
        all_files = os.listdir()  # List all files in main directory
        if self.file_name not in all_files:
            # If the file does not exist, create it
            with open(self.file_name, mode="w", encoding="utf-8") as file:
                csv_writer = csv.writer(file)
                csv_writer.writerow(
                    [
                        "Time",
                        "Temperature",
                        "Humidity",
                        "Pressure",
                        "Altitude",
                        "Acceleration",
                        "Gyro",
                        "Magnetometer",
                    ]
                )

    def log(self, temp, humidity, pressure, altitude, acceleration, gyro, magnetometer):

        # Append data to buffer
        self.buffer.append(
            f'{time.monotonic()},{temp},{humidity},{pressure},{altitude},"{acceleration}","{gyro}","{magnetometer}"'
        )
        
        print(gc.mem_free())

        if len(self.buffer) >= int(LOG_BUFFER_LENGTH) and gc.mem_free() > int(MIN_RAM_BEFORE_CLEAR):
            # If the buffer is full, write the data to the CSV file
            with open(self.file_name, mode="a", encoding="utf-8") as file:

                for data in self.buffer:
                    file.write(data + "\n")
                                    
                # Clear the buffer
                self.buffer = []
