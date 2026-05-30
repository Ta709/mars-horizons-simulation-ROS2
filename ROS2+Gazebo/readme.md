# ROS 2 Jazzy & Gazebo Sim WSL2 Troubleshooting Log

This repository documents the environment quirks, networking blockades, and custom workarounds discovered while setting up **ROS 2 Jazzy (Geochelone)** and **Gazebo Sim (Harmonic / gz-sim8)** inside a **Windows Subsystem for Linux (WSL2)** Ubuntu environment on an HP Laptop.

---

## 💻 My Environment Setup
* **Host Machine:** HP Laptop (Windows 11)
* **Linux Layer:** WSL2 (Native Ubuntu Terminal App)
* **ROS 2 Version:** Jazzy Jalisco (`/opt/ros/jazzy`)
* **Simulator:** Gazebo Sim Harmonic (`gz-sim8`)

---

## ❌ What DID NOT Work (The Roadblocks)

### 1. Mixed Windows Terminal Hosts (PowerShell vs. CMD vs. WSL)
* **The Situation:** Running Gazebo in a WSL instance hosted via PowerShell, while running the keyboard node in a WSL instance hosted via CMD.
* **Why it failed:** Even though both were Linux under the hood, mixing Windows host wrappers isolated the internal virtual network layers. ROS 2 nodes were completely blind to each other across the boundaries.

### 2. Default Short-Path World Launches (`gz sim -r diff_drive.sdf`)
* **The Situation:** Typing the short-path command caused Gazebo to either crash with a `Segmentation fault (Signal sent by the kernel)` inside `gz::transport::v13::Discovery` or silently fail and open a completely blank world.
* **Why it failed:** 1. WSL firewall rules initially glitched the network discovery environment variables (`GZ_IP`, etc.), causing `getenv` memory segments to crash the simulator engine on launch.
  2. Gazebo Harmonic handles short-path indexing differently; when it couldn't locate the file locally, it pulled down a default fallback empty layout instead of the actual car model.

### 3. High Linear Velocities (> 3.0 m/s) inside WSL
* **The Situation:** Once the bridge connected, sending a high speed command (4.4 m/s) made both robot cars glitch violently, stuttering between two physical positions back and forth simultaneously.
* **Why it failed:** This caused a virtual "quantum superposition" visual effect. Because WSL shares CPU/GPU threads laggingly with Windows, a massive velocity vector overwhelmed the simulation's low real-time physics refresh rate, causing severe tire slip calculations and rendering delays.

---

##  What DID Work (The Solutions)

To successfully drive a 3D robot using an external ROS 2 node into Gazebo Sim over WSL2, the following exact configuration sequence must be used:

### Step 1: Wipe Glitched Network Variables
Before launching, clear the broken network discovery environment variables to prevent the background communication transport layer from crashing:
```bash
unset GZ_RELAY_ADDR GZ_IP GZ_PARTITION