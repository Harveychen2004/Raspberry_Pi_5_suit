# MQ2 Module #

## Hardware Equipment:

- Raspberry Pi 5 board
- Power adapter
- 40-pin ribbon cable
- MQ2 Sensor
- MCP3008 Digital-Analog converter
- Jumpers

## Circuit Diagram:
| Raspberry Pi | T board | MCP3008 |
| :----------: | ------- | ------- |
|     3.3v     | 3.3v    | 3.3v    |
|     GND      | GND     | GND     |
|     CE0      | CE0     | CE0     |
|     MOSI     | MOSI    | MOSI    |
|     MISO     | MISO    | MISO    |
|     SCK      | SCK     | SCK     |

| MQ2  | T board | MCP3008 |
| :--: | ------- | ------- |
|  DO  | GPIO16  | \       |
|  AO  | \       | AISO    |
| VCC  | 5v      | \       |
| GND  | GND     | \       |



## Sample Output:
![image](https://github.com/user-attachments/assets/3f568e36-cea9-4f2f-963b-1ea952466f6a)

