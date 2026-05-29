# 🛰️ Mars Horizons Space Network Simulation

An advanced robotics simulation bridging a native **Windows UCRT64** ground control hub to a remote **Raspberry Pi ROS 2** exploration environment over a custom socket network.

## 🚀 Features
* **Deep Space Network Lag:** Simulates a 1.0-second speed-of-light radio packet delay via thread-safe Python processing queues.
* **ASCII Radar Map:** Features a dynamic telemetry parsing engine that draws a clean visual crater grid natively in the UCRT64 terminal.
* **Autonomous Safety Protocols:** Edge-computing obstacle tracking blocks movement actions that would cause collisions with Martian boulders.
* **Multithreaded Telemetry Async:** Implements background worker sockets so ground control input typing is never overwritten by data loops.

## 📂 Project Structure
* `earth_control/` - Native Windows Python application interface.
* `mars_rover_node/` - Python-based ROS 2 package tracking virtual coordinates, hazard states, and core sampling instrumentation.

## 🛠️ Execution
1. Run `ros2 run mars_simulation rover_node` on your robot system.
2. Launch `python earth_control/earth_control.py` on your Windows UCRT64 control deck.
