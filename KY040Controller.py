from gpiozero import RotaryEncoder, Button
from time import sleep
import threading
from TGS2620Sensor import TGS2620Sensor
from MQ2Sensor import MQ2Sensor
from MAX30102Sensor import MAX30102Sensor
from MPU6050Sensor import MPU6050Sensor

class KY040Controller:
    def __init__(self):
        self.encoder = RotaryEncoder(a=6, b=5)  # CLK连接GPIO6，DT连接GPIO5
        self.button = Button(12)                # SW连接 GPIO12
        self.globalCounter = 0                  # 计数器值
        self.tmp = 0                            # 当前状态判断
        self.running = False

        # 模式列表
        self.TGS2620 = TGS2620Sensor()
        self.MQ2 = MQ2Sensor()
        self.MAX30102 = MAX30102Sensor()
        self.MPU6050 = MPU6050Sensor()
        self.modes = ["MPU6050", "MAX30102", "MQ2", "TGS2620", "Start All", "Shut Down All"]
        self.start_modes = ["Start MPU6050", "Start MAX30102", "Start MQ2", "Start TGS2620", "Start All", "Shut Down All"]
        self.run_modes = [self.MPU6050.run, self.MAX30102.run, self.MQ2.run, self.TGS2620.run, None, None]
        self.stop_modes = [self.MPU6050.stop, self.MAX30102.stop, self.MQ2.stop, self.TGS2620.stop, None, None]
        self.threads = {}

        # 设置按键中断
        self.button.when_pressed = self.btnISR

    def rotaryDeal(self):
        """旋转编码方向位判断函数"""
        self.globalCounter += self.encoder.steps  # 根据编码器步骤调整计数器
        self.encoder.steps = 0  # 更新计数器后重置编码器步骤
        if self.tmp != self.globalCounter:  # 判断状态值发生改变
            mode_index = self.globalCounter % len(self.modes)
            print(f"Mode: {self.modes[mode_index]}")  # 打印出状态信息
            self.tmp = self.globalCounter  # 把当前状态赋值到下一个状态，避免重复打印

    def btnISR(self):
        """中间按键按下响应程序"""
        mode_index = self.globalCounter % len(self.start_modes)

        if self.run_modes[mode_index] and self.stop_modes[mode_index]:
            if mode_index not in self.threads or not self.threads[mode_index].is_alive():
                thread = threading.Thread(target=self.run_modes[mode_index], daemon=True)
                self.threads[mode_index] = thread
                thread.start()
                print(self.start_modes[mode_index])
            else:
                print(f"{self.modes[mode_index]} is already running")
                self.stop_modes[mode_index]()
                self.threads[mode_index].join()
                print(f"{self.modes[mode_index]} killed")

        sleep(1)  # 防抖

    def run(self):
        """主运行逻辑"""
        try:
            self.running = True
            print("run")
            while self.running:
                self.rotaryDeal()  # 更新编码器值
                sleep(0.01)        # 短延迟，降低CPU负载
        except KeyboardInterrupt:
            print(self.threads)
            pass

if __name__ == '__main__':
    controller = KY040Controller()
    controller.run()