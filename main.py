import threading
from gpiozero import Button
from time import sleep
from KY040Controller import KY040Controller

# 初始化按钮和 KY040Controller
btn = Button(17)  # 轻触按键管脚
controller = KY040Controller()
controller_running = False  # 标志位，控制 KY040Controller 的运行状态

def toggle_controller():
    global controller_running
    if not controller_running:
        print("KY040Controller started")
        controller_running = True
        threading.Thread(target=controller.run, daemon=True).start()
    else:
        print("KY040Controller stopped")
        controller_running = False
        controller.running = False  # 停止 KY040Controller 的主循环

# 设置按钮按下时调用的函数
btn.when_pressed = toggle_controller

# 保持程序运行
print("Press the button to start or stop the KY040Controller.")
try:
    while True:
        sleep(0.5)
except KeyboardInterrupt:
    print("\nProgram terminated by user.")
