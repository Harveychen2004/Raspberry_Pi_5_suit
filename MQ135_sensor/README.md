# MQ135 Module #

## Overview:

The MQ-135 is a widely used air quality sensor capable of detecting a variety of **harmful gases and volatile organic compounds (VOCs)**. It is commonly used in indoor air quality monitoring, pollution detection, and environmental health projects. This characteristic make it an ideal sensor to detect smoking behavior of driver. It outputs an **analog voltage** corresponding to gas concentration and is suitable for integration with an external ADC (like MCP3008) when used with Raspberry Pi.

## Working Principle:

The MQ-135 uses a **SnO₂ (tin dioxide) semiconductor** layer whose resistance changes in the presence of certain gases. By measuring the voltage across the load resistor (RL), you can estimate the gas concentration.
It is sensitive to gases such as:
- Carbon monoxide (CO)
- Ammonia (NH₃)
- Benzene (C₆H₆)

## Hardware Equipment:

- Raspberry Pi 5 board
- Power adapter
- 40-pin ribbon cable
- MQ135 Sensor
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

| MQ-135 Pin | Description        | Connection                   |
|------------|--------------------|-------------------------------|
| VCC        | Power Input (5V)   | Raspberry Pi 5V               |
| GND        | Ground             | Raspberry Pi GND              |
| AOUT       | Analog Output      | MCP3008 CH0 input pin         |
| DOUT       | Digital Output     | GPIO 16                       |

## Technical Specification:

| Parameter        | Value                                      |
|------------------|--------------------------------------------|
| Interface        | Analog output (AOUT) + Digital output (DOUT) |
| Supply Voltage   | 5V                                         |
| Heater Voltage   | 5V (±0.1V)                                 |
| Preheat Time     | ≥ 1 min for heating                       |
| Detection Range  | 10 ppm – 1000 ppm (approximate, gas-specific) |
| Sensitivity Gases | NH₃, NOx, Alcohol, Benzene, CO      |

## Sample Output:
![image](https://github.com/user-attachments/assets/3f568e36-cea9-4f2f-963b-1ea952466f6a)

