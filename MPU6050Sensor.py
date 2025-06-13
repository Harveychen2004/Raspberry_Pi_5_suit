import time
import smbus
import pandas as pd

class MPU6050Sensor:
    GRAVITY_MS2 = 9.80665

    # Scale Modifiers
    ACCEL_SCALE_MODIFIER_2G = 16384.0
    ACCEL_SCALE_MODIFIER_4G = 8192.0
    ACCEL_SCALE_MODIFIER_8G = 4096.0
    ACCEL_SCALE_MODIFIER_16G = 2048.0

    GYRO_SCALE_MODIFIER_250DEG = 131.0
    GYRO_SCALE_MODIFIER_500DEG = 65.5
    GYRO_SCALE_MODIFIER_1000DEG = 32.8
    GYRO_SCALE_MODIFIER_2000DEG = 16.4

    # Pre-defined ranges
    ACCEL_RANGE_2G = 0x00
    ACCEL_RANGE_4G = 0x08
    ACCEL_RANGE_8G = 0x10
    ACCEL_RANGE_16G = 0x18

    GYRO_RANGE_250DEG = 0x00
    GYRO_RANGE_500DEG = 0x08
    GYRO_RANGE_1000DEG = 0x10
    GYRO_RANGE_2000DEG = 0x18

    # MPU-6050 Registers
    PWR_MGMT_1 = 0x6B
    ACCEL_XOUT0 = 0x3B
    ACCEL_YOUT0 = 0x3D
    ACCEL_ZOUT0 = 0x3F
    TEMP_OUT0 = 0x41
    GYRO_XOUT0 = 0x43
    GYRO_YOUT0 = 0x45
    GYRO_ZOUT0 = 0x47
    ACCEL_CONFIG = 0x1C
    GYRO_CONFIG = 0x1B

    def __init__(self, address=0x68, bus=1):
        self.address = address
        self.bus = smbus.SMBus(bus)
        self.data = []
        self.running = False

        # Wake up the MPU-6050 since it starts in sleep mode
        self.bus.write_byte_data(self.address, self.PWR_MGMT_1, 0x00)

    def read_i2c_word(self, register):
        high = self.bus.read_byte_data(self.address, register)
        low = self.bus.read_byte_data(self.address, register + 1)
        value = (high << 8) + low
        if value >= 0x8000:
            return -((65535 - value) + 1)
        else:
            return value

    def get_accel_data(self):
        x = self.read_i2c_word(self.ACCEL_XOUT0)
        y = self.read_i2c_word(self.ACCEL_YOUT0)
        z = self.read_i2c_word(self.ACCEL_ZOUT0)

        accel_range = self.bus.read_byte_data(self.address, self.ACCEL_CONFIG)
        if accel_range == self.ACCEL_RANGE_2G:
            scale_modifier = self.ACCEL_SCALE_MODIFIER_2G
        elif accel_range == self.ACCEL_RANGE_4G:
            scale_modifier = self.ACCEL_SCALE_MODIFIER_4G
        elif accel_range == self.ACCEL_RANGE_8G:
            scale_modifier = self.ACCEL_SCALE_MODIFIER_8G
        elif accel_range == self.ACCEL_RANGE_16G:
            scale_modifier = self.ACCEL_SCALE_MODIFIER_16G
        else:
            scale_modifier = self.ACCEL_SCALE_MODIFIER_2G

        x = (x / scale_modifier) * self.GRAVITY_MS2
        y = (y / scale_modifier) * self.GRAVITY_MS2
        z = (z / scale_modifier) * self.GRAVITY_MS2

        return {'x': x, 'y': y, 'z': z}

    def get_gyro_data(self):
        x = self.read_i2c_word(self.GYRO_XOUT0)
        y = self.read_i2c_word(self.GYRO_YOUT0)
        z = self.read_i2c_word(self.GYRO_ZOUT0)

        gyro_range = self.bus.read_byte_data(self.address, self.GYRO_CONFIG)
        if gyro_range == self.GYRO_RANGE_250DEG:
            scale_modifier = self.GYRO_SCALE_MODIFIER_250DEG
        elif gyro_range == self.GYRO_RANGE_500DEG:
            scale_modifier = self.GYRO_SCALE_MODIFIER_500DEG
        elif gyro_range == self.GYRO_RANGE_1000DEG:
            scale_modifier = self.GYRO_SCALE_MODIFIER_1000DEG
        elif gyro_range == self.GYRO_RANGE_2000DEG:
            scale_modifier = self.GYRO_SCALE_MODIFIER_2000DEG
        else:
            scale_modifier = self.GYRO_SCALE_MODIFIER_250DEG

        x = x / scale_modifier
        y = y / scale_modifier
        z = z / scale_modifier

        return {'x': x, 'y': y, 'z': z}

    def read_temperature(self):
        temp_raw = self.read_i2c_word(self.TEMP_OUT0)
        temperature = (temp_raw / 340.0) + 36.53
        return temperature

    def log_data(self, accel_data, gyro_data, temp, current_time):
        self.data.append({
            'Time': current_time,
            'Accelerometer_x': accel_data['x'],
            'Accelerometer_y': accel_data['y'],
            'Accelerometer_z': accel_data['z'],
            'Gyroscope_x': gyro_data['x'],
            'Gyroscope_y': gyro_data['y'],
            'Gyroscope_z': gyro_data['z'],
            'Temperature': temp
        })

    def save_data(self, file_path="data/MPU6050.csv"):
        df = pd.DataFrame(self.data)
        df.to_csv(file_path, index=False)

    def run(self):
        try:
            self.running = True
            while self.running:
                current_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
                accel_data = self.get_accel_data()
                gyro_data = self.get_gyro_data()
                temp = self.read_temperature()

                self.log_data(accel_data, gyro_data, temp, current_time)
                time.sleep(0.5)
        except KeyboardInterrupt:
            print("Keyboard Interruption")
        finally:
            self.save_data()

    def stop(self):
        if self.running:
            self.running = False
        else:
            print("Error")

if __name__ == '__main__':
    sensor = MPU6050Sensor()
    sensor.run()