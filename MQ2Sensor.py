from gpiozero import Button, MCP3008
import time
import pandas as pd

class MQ2Sensor:
    def __init__(self, digital_pin=16, analog_channel=0):
        self.DO = Button(digital_pin)               # 数字输出引脚
        self.GasPin = MCP3008(channel=analog_channel)  # 模拟通道
        self.status = 1                             # 当前传感器状态（1表示安全）
        self.count = 0                              # 累计危险时间
        self.state_label = ["Dangerous", "Safe"]
        self.data = []                              # 数据记录列表
        self.running = False

    @staticmethod
    def map_value(x, in_min, in_max, out_min, out_max):
        return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

    def display_status(self, status):
        if status == 1:
            print('\n   ******************')
            print('   * Makerobo Safe~ *')
            print('   ******************\n')
        elif status == 0:
            print('\n   ************************')
            print('   * Makerobo Danger Gas! *')
            print('   ************************\n')

    def read_sensor(self):
        raw_value = self.GasPin.value
        processed_value = round(self.map_value(raw_value, 0, 1, 0, 255))
        danger = not self.DO.is_pressed
        return raw_value, processed_value, danger

    def log_data(self, time_str, raw_val, processed_val, status):
        self.data.append({
            'Time': time_str,
            'Initial Gas Value': raw_val,
            'Processed Gas Value': processed_val,
            'State': self.state_label[status],
            'Warning time period(s)': self.count
        })

    def save_data(self, save_path="data/MQ2.csv"):
        df = pd.DataFrame(self.data)
        df.to_csv(save_path, index=False)

    def run(self):
        try:
            print("MQ2 run\n")
            self.running = True
            while self.running == True:
                current_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
                raw_val, processed_val, danger = self.read_sensor()

                # print(f"Gas Value: {processed_val}")
                # print(f"Initial volume: {raw_val}")

                if danger != self.status:
                    self.display_status(danger)
                    self.status = danger

                if danger:
                    self.count += 1
                else:
                    self.count = 0

                self.log_data(current_time, raw_val, processed_val, self.status)
                time.sleep(1)    
        except KeyboardInterrupt:
            print("Keyboard Interruption")
        finally:
            self.save_data()

    def stop(self):
        if self.running == True:
            self.running = False
        else:
            print("Error")

if __name__ == '__main__':
    sensor = MQ2Sensor()
    sensor.run()