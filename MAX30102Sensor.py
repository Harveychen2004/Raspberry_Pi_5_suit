import time
import pandas as pd
from heartrate_monitor import HeartRateMonitor

class MAX30102Sensor:
    def __init__(self, duration=10, print_raw=False, print_result=True):
        self.duration = duration
        self.sensor = HeartRateMonitor(print_raw=print_raw, print_result=print_result)
        self.data = []
        self.running = False

    def start_sensor(self):
        self.sensor.start_sensor()

    def stop_sensor(self):
        self.sensor.stop_sensor()

    def get_sensor_data(self):
        return self.sensor.get_data()

    def save_data(self, file_path="data/MAX30102.csv"):
        df = pd.DataFrame(self.data)
        df.to_csv(file_path, index=False)

    def run(self):
        try:
            self.running = True
            self.start_sensor()
            # print("Sensor started.")
            start_time = time.time()
            # while self.running and (time.time() - start_time < self.duration):
            #     time.sleep(1)  # Simulate data collection interval
            while self.running:
                time.sleep(1)  # Simulate data collection interval
            self.data = self.get_sensor_data()
            # print("Data collection complete.")
        except KeyboardInterrupt:
            print("Keyboard Interruption")
        finally:
            self.stop_sensor()
            self.save_data()

    def stop(self):
        if self.running:
            self.running = False
        else:
            print("Error")

if __name__ == '__main__':
    sensor = MAX30102Sensor(duration=10)
    sensor.run()