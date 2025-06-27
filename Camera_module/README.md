# Raspberry Pi NOIR V3 Wide Camera Module with Dual-Servo Face Tracking #

## Overview

This module integrates a **Raspberry Pi Camera V3 NOIR Wide** with a **dual-servo gimbal system** (controlled via **PCA9685 PWM driver**), enabling real-time **driver face tracking** and **facial motion analysis**. It serves as a core component in the intelligent driving system, allowing detection of distracted or fatigued driver behaviors.

The camera's physical orientation is controlled by:
- **Tilt servo** — vertical tracking
- **Gimbal servo** — horizontal tracking

Together with facial analysis algorithms, the system tracks head movements and monitors driver alertness.

## Objectives

- Track the driver’s face in real time  
- Detect facial cues indicating **drowsiness, distraction, or fatigue**, such as:
  - Head nodding
  - Eye closure or blinking frequency
  - Yawning
  - Looking away from the road (left/right)

### 🧠 Software Algorithms

| Task                          | Technology Used                             |
|-------------------------------|---------------------------------------------|
| **Face Detection**            | HAAR Cascade Classifier (OpenCV)            |
| **Facial Landmark Detection** | MediaPipe `face_landmarker` Model           |
| **Behavior Detection**        | Landmark-based logic for nodding, yawning, etc. |

- The **HAAR model** provides fast and lightweight face localization
- The **Mediapipe model** enables precise detection of eye, mouth, and head movement

### ⚙️ Hardware Components

| Component                    | Description                                   |
|------------------------------|-----------------------------------------------|
| Camera Module                | Raspberry Pi Camera V3 NOIR Wide              |
| Servo Controller             | PCA9685 PWM Driver (I2C interface)            |
| Servo Motors (x2)            | Controls camera tilt (vertical) and pan (horizontal) |

> 📌 The NOIR camera has no IR filter, enhancing visibility in **low-light environments**, ideal for night driving monitoring.

### 🛠️ Raspberry Pi Wiring (PCA9685 + Camera)

| Device         | Pin            | Raspberry Pi GPIO (BCM) | Description                |
|----------------|----------------|--------------------------|----------------------------|
| PCA9685        | SDA            | GPIO2 (SDA)              | I²C Data                   |
| PCA9685        | SCL            | GPIO3 (SCL)              | I²C Clock                  |
| PCA9685        | VCC            | 3.3V or 5V               | Power Supply               |
| PCA9685        | GND            | GND                      | Ground                     |
| Camera Module  | Ribbon Cable   | CSI Port                 | Connects to Pi Camera Port |