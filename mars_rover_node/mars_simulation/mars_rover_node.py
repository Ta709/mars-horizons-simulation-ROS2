import rclpy
from rclpy.node import Node
from std_msgs.msg import String
import socket
import threading
import random
import time
import queue

class MarsRoverNode(Node):
    def __init__(self):
        super().__init__('mars_rover')
        
        # Virtual Mars Environment Setup (Jezero Crater Grid)
        self.mars_map = {
            (2.0, 3.0): "⚠️ BOULDER FIELD",
            (-1.0, 4.0): "⏳ DEEP SAND PIT",
            (3.0, 5.0): "💎 SCIENTIFIC ANOMALY: Clay Minerals (Potential Biosignature)",
            (-2.0, -2.0): "💎 SCIENTIFIC ANOMALY: Subsurface Water Ice Peak",
            (0.0, 5.0): "⚠️ CRATER RIM DROP-OFF"
        }
        
        # Rover Internal Systems
        self.x, self.y = 0.0, 0.0
        self.battery = 100
        self.solar_charging = True
        self.status = "SYSTEMS ONLINE - Awaiting Ground Control Link"
        self.science_cache = []
        self.is_drilling = False
        
        # Deep Space Signal Delay Queue (1.0 Second Speed-of-Light Lag)
        self.command_queue = queue.Queue()
        self.SIGNAL_DELAY = 1.0  
        
        # Network Engine
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind(('0.0.0.0', 5005))
        self.server_socket.listen(1)
        self.conn = None
        
        # Background threads
        threading.Thread(target=self.wait_for_earth, daemon=True).start()
        threading.Thread(target=self.process_delay_queue, daemon=True).start()
        
        self.timer = self.create_timer(2.0, self.send_telemetry)
        self.get_logger().info("🔥 Advanced Mars Exploration Engine with Signal Delay Initialized.")

    def wait_for_earth(self):
        self.conn, addr = self.server_socket.accept()
        self.get_logger().info(f"🛰️ Deep Space Network Link Active with Earth: {addr}")
        while True:
            try:
                data = self.conn.recv(1024).decode('utf-8').strip().lower()
                if not data: break
                
                arrival_time = time.time()
                self.send_string_to_earth(f"📡 [DSN INFO] Transmission intercepted. Packet traveling through space ({self.SIGNAL_DELAY}s lag)...")
                self.command_queue.put((data, arrival_time))
            except:
                break

    def process_delay_queue(self):
        while True:
            try:
                cmd, arrival_time = self.command_queue.get(timeout=0.1)
                time_elapsed = time.time() - arrival_time
                remaining_delay = self.SIGNAL_DELAY - time_elapsed
                
                if remaining_delay > 0:
                    time.sleep(remaining_delay)
                
                if self.is_drilling:
                    self.send_string_to_earth("❌ COMMAND REJECTED: Robotic arm deployed. Drilling operations in progress.")
                    continue
                self.process_mission_command(cmd)
            except queue.Empty:
                continue

    def send_string_to_earth(self, text):
        if self.conn:
            try:
                self.conn.send((text + "\n").encode('utf-8'))
            except:
                self.conn = None

    def send_telemetry(self):
        if self.battery > 0:
            if not self.is_drilling:
                self.battery -= 0.5 if not self.solar_charging else 0.1
        else:
            self.status = "💀 CRITICAL ERROR: SYSTEM POWER DEAD"

        radar_report = "Scan Clear"
        for hazard_pos, hazard_type in self.mars_map.items():
            dist = ((self.x - hazard_pos[0])**2 + (self.y - hazard_pos[1])**2)**0.5
            if dist <= 1.5:
                radar_report = f"🚨 PROXIMITY ALERT: {hazard_type} detected nearby!"

        report = (
            f"\n====== 🛰️ MARS TELEMETRY PACKET ======\n"
            f"📍 Position: [X: {self.x}, Y: {self.y}]\n"
            f"🔋 Core Power: {int(self.battery)}% | Status: {self.status}\n"
            f"📡 Sensors: {radar_report}\n"
            f"📦 Collected Samples: {len(self.science_cache)} items in storage\n"
            f"======================================"
        )
        self.send_string_to_earth(report)

    def process_mission_command(self, cmd):
        self.get_logger().info(f"Executing Delayed Ground Control Payload: '{cmd}'")
        
        if "move" in cmd:
            target_x, target_y = self.x, self.y
            if "forward" in cmd: target_y += 1.0
            elif "back" in cmd: target_y -= 1.0
            elif "left" in cmd: target_x -= 1.0
            elif "right" in cmd: target_x += 1.0
            
            if (target_x, target_y) in self.mars_map and "⚠️" in self.mars_map[(target_x, target_y)]:
                self.status = "🚫 AUTONOMOUS EMERGENCY STOP EXECUTION"
                self.send_string_to_earth(f"⛔ MOVEMENT ABORTED: Path blocked by {self.mars_map[(target_x, target_y)]}!")
            else:
                self.x, self.y = target_x, target_y
                self.status = "EXECUTING TRANSIT MANEUVER"

        elif "drill" in cmd:
            current_pos = (self.x, self.y)
            if current_pos in self.mars_map and "💎" in self.mars_map[current_pos]:
                self.is_drilling = True
                threading.Thread(target=self.run_drill_sequence, args=(self.mars_map[current_pos],), daemon=True).start()
            else:
                self.send_string_to_earth("⚠️ DRILL FAILURE: Sensors indicate nothing but barren basalt here. Save your power.")
                
        elif "status" in cmd:
            self.status = "SYSTEMS HEALTH CHECK COMPLETED (100% NOMINAL)"
        else:
            self.status = f"ECHO: Command '{cmd}' registered but unhandled."

    def run_drill_sequence(self, anomaly_name):
        self.status = "⚙️ DRILLING OPERATION ACTIVE - DO NOT MOVE"
        for i in range(3, 0, -1):
            self.send_string_to_earth(f"⏳ Extracting core sample... {i}s remaining")
            time.sleep(1)
        
        sample_id = f"Sample_{random.randint(1000,9999)}"
        self.science_cache.append(sample_id)
        self.send_string_to_earth(f"🎉 SUCCESS! Secured core matrix from: {anomaly_name}. Cached as {sample_id}.")
        del self.mars_map[(self.x, self.y)]
        self.is_drilling = False
        self.status = "IDLE (Science operations completed)"

def main(args=None):
    rclpy.init(args=args)
    node = MarsRoverNode()
    try: rclpy.spin(node)
    except KeyboardInterrupt: pass
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
