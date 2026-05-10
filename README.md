# 🚲 Road Incident Detector

An open-source bike-mounted road incident detection system built with Arduino and Python. As you ride, the system automatically detects potholes using a machine learning model running on a camera, alerts you in real time through LEDs and a buzzer, logs every incident with GPS coordinates and a snapshot, and uploads everything to a road-incident API when you park.

---

## How It Works

The system is split across two layers that communicate through a serial bridge:

**Arduino side (`sketch.ino`)** handles all the hardware. On boot, the movement modulino takes 50 accelerometer samples to calibrate a baseline. From that point on, it continuously compares live acceleration readings against the baseline — if the delta exceeds 0.15 g on any axis, it declares the bike in motion and tells Python to activate the camera. When the bike stays still for more than 2 seconds, it signals Python to pause detection. While riding, if Python reports a pothole was detected, the Arduino lights up the pixel LEDs in red (one LED per pothole) and fires the buzzer, with a 5-second cooldown between alerts to avoid spam. Pressing the knob triggers the "end of trip" sequence.

**Python side (`main.py`)** handles the intelligence. It runs a video object detection model watching the camera feed. When the Arduino says the bike is moving, detections are processed: each pothole or critical road damage event is saved to a local SQLite database (`viatges.db`) with a label, confidence score, timestamp, simulated GPS coordinates, and a base64-encoded frame snapshot. It also pushes live detection events to a web UI. When the knob is pressed, Python reads all stored records, posts them one by one to the road-incident API, clears the database, and shuts the app down.

```
┌─────────────────────────────────────────────────────────────┐
│                        Bike Riding                          │
│                                                             │
│  Movement Modulino → Motion detected → Camera activates     │
│         ↓                                                   │
│  ML Model sees pothole → Saved to SQLite + LED + Buzzer     │
│         ↓                                                   │
│  Knob pressed → All records POSTed to API → App stops       │
└─────────────────────────────────────────────────────────────┘
```

---

## Hardware Requirements

- Arduino Uno Q
- [Arduino Modulino](https://docs.arduino.cc/hardware/modulino/) — the following modules are required:
  - **Movement** (IMU accelerometer for motion detection)
  - **Pixels** (LED strip for pothole alerts)
  - **Buzzer** (audio alert on pothole detection)
  - **Knob** (press to end the trip and upload data)
- A USB webcam / facecam connected to the host machine

---

## Software Requirements

- [Arduino AppLab](https://app.arduino.cc/) installed on your computer
- Arduino AppLab CLI installed

---

## Setup & Installation

### 1. Install the pothole detection model

The camera relies on a custom Edge Impulse model trained to detect potholes and critical road damage. Install it from:

👉 [https://studio.edgeimpulse.com/public/992115/live](https://studio.edgeimpulse.com/public/992115/live)

Follow the Edge Impulse deployment instructions to make the model available to Arduino AppLab's Video Object Detection brick.

### 2. Clone the repository via AppLab CLI

Open a terminal and run:

```bash
applab clone <your-repo-url>
```

### 3. Open the project

```bash
applab open .
```

This will launch the project inside the Arduino AppLab environment.

### 4. Connect your hardware

Plug in your Arduino Uno Q and attach all four Modulinos (Movement, Pixels, Buzzer, Knob). Make sure the facecam is also connected.

### 5. Run the project

Hit **Run** inside AppLab. The system will calibrate the movement sensor on startup (keep the board still for ~2 seconds) and then print `🚀 Sistema iniciat! Esperant moviment...` when ready.

---

## Usage

| Action | Result |
|---|---|
| Start riding | Motion detected → camera activates automatically |
| Pothole detected | LEDs turn red, buzzer fires, incident saved locally |
| Stop riding | Camera pauses after 2 seconds of stillness |
| Press the Knob | All incidents uploaded to API, app shuts down |

---

## Troubleshooting

**AppLab says a brick is missing**
Remove the brick that is flagged as missing from your AppLab project, then re-add it. After re-adding, reinstall the pothole detector model from Edge Impulse:
👉 [https://studio.edgeimpulse.com/public/992115/live](https://studio.edgeimpulse.com/public/992115/live)

**No motion detected even while moving**
The sensor calibrates on boot. Make sure the board is held completely still for the first 2 seconds after powering on, otherwise the baseline will be off and the threshold comparisons won't work correctly.

**Camera feed not starting**
Make sure the facecam is connected before launching the app. AppLab needs to detect the camera device at startup.

**API upload fails at end of trip**
The local SQLite database (`viatges.db`) is not cleared if the upload fails, so your data is safe. Check your network connection and try pressing the knob again on the next run — the app will attempt to resend all stored records.

---

## License

This project is licensed under the **MIT License**.

```
MIT License

Copyright (c) 2026 Contributors

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```
