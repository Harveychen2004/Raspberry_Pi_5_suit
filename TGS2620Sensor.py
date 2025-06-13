import time
import pandas as pd
from gpiozero import Button, MCP3008

class TGS2620Sensor:
    def __init__(self, analog_channel=1, digital_pin=13):
        self.analog_pin = MCP3008(channel=analog_channel)
        self.digital_pin = Button(digital_pin)
        self.data = []
        self.state = ["Dangerous", "Safe"]
        self.status = 1
        self.count = 0
        self.running = False
    
    @staticmethod
    def map_value(x, in_min, in_max, out_min, out_max):
        return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

    def read_sensor(self):
        init_val = self.analog_pin.value
        processed_val = round(self.map_value(init_val, 0, 1, 0, 1000))
        return init_val, processed_val

    def log_data(self, init_val, processed_val, current_time):
        self.data.append({
            'Time': current_time,
            "Initial Alcohol Value": init_val,
            "Processed Alcohol Value": processed_val,
            "State": self.state[self.status],
            "Warning time period(s)": self.count
        })

    def save_data(self, file_path="data/TGS2620.csv"):
        df = pd.DataFrame(self.data)
        df.to_csv(file_path, index=False)

    def run(self):
        try:
            self.running = True
            while self.running == True:
                current_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
                init_val, processed_val = self.read_sensor()
                
                # print('Alcohol Value:', processed_val)

                tmp_status = not self.digital_pin.is_pressed
                if tmp_status != self.status:
                    print(tmp_status)
                    self.status = tmp_status

                if self.status == 0:
                    self.count += 1
                else:
                    self.count = 0

                self.log_data(init_val, processed_val, current_time)
                time.sleep(1)             
            self.save_data()
        except KeyboardInterrupt:
            self.save_data()
            print("Exit")

    def stop(self):
        if self.running == True:
            self.running = False
        else:
            print("Error")

if __name__ == '__main__':
    sensor = TGS2620Sensor()
    sensor.run()