# MCP3008 10-Bit 8-Channel Analog-to-Digital Converter (ADC) #

## Overview

The `MCP3008` is a widely used **10-bit analog-to-digital converter** (ADC) that allows Raspberry Pi and other digital platforms to read **analog voltage signals**. It provides **8 independent input channels**, making it ideal for integrating analog sensors i.e. **MQ gas sensors**, **TGS sensors** with the Raspberry Pi. It communicates via the **SPI protocol**, ensuring fast and reliable analog data conversion in real time.

## Working Principle

Raspberry Pi lacks native analog input pins. The MCP3008 solves this by acting as an **interface between analog sensors and digital GPIO-based devices**, converting a voltage signal (0~3.3V or 0~5V depending on supply) into a **10-bit digital value (0～1)**.

## Technical Specifications

| Parameter        | Value                                |
|------------------|--------------------------------------|
| Interface        | SPI (Serial Peripheral Interface)    |
| Input Channels   | 8 (CH0 to CH7)                       |
| Resolution       | 10-bit                               |
| Input Voltage    | 3.3V                                 |
| Supply Voltage   | 2.7V to 5.5V                         |
| Conversion Time  | ~2.5 µs                              |
| Modes            | Single-ended                         |
| Package          | DIP-16 / SOIC                        |

## Circuit Diagram

| MCP3008 Pin | Description        | Raspberry Pi GPIO (BCM) | 
|-------------|--------------------|--------------------------|
| VDD         | Power (3.3V or 5V) | 3.3V                     | 
|  GND        | Analog Ground      | GND                      | 
| SCK         | SPI Clock          | GPIO11 (SPI0_SCK)        | 
| DOUT        | SPI MISO           | GPIO9  (SPI0_MISO)       |
| DIN         | SPI MOSI           | GPIO10 (SPI0_MOSI)       |
| CS/SHDN     | Chip Select        | GPIO8  (SPI0_CE0)        | 