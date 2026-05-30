import socket
import sys
import threading
import os
import time

# IP address of your Raspberry Pi on your local network
PI_IP = "192.168.0.102"  
PORT = 5005

# Coordinates map for display rendering on Earth
OBSTACLES = {
    (2.0, 3.0): "⚠️",   # Boulder Field
    (-1.0, 4.0): "⏳",  # Deep Sand Pit
    (3.0, 5.0): "💎",   # Clay Minerals Anomaly
    (-2.0, -2.0): "💎", # Subsurface Ice Anomaly
    (0.0, 5.0): "⚠️"    # Crater Rim
}

# Track last known positions to prevent unnecessary screen flashing
last_x, last_y = 0.0, 0.0

def render_map(rover_x, rover_y):
    """Draws an ASCII radar grid of the Martian surface aligned to a compass."""
    print("\n--- 🗺️ JEZERO CRATER RADAR MAP ---")
    # Loop from Y=6 down to Y=-3, and X=-4 to X=3 to build an 8x8 grid
    for y in range(6, -4, -1):
        row_str = "  "
        for x in range(-4, 4):
            pos = (float(x), float(y))
            if float(x) == rover_x and float(y) == rover_y:
                row_str += "🤖 "  # The Rover
            elif pos in OBSTACLES:
                row_str += OBSTACLES[pos] + " "
            else:
                row_str += "· "  # Empty Martian Soil
        print(row_str)
    print("---------------------------------")
    print("Legend: 🤖=Rover | ⚠️=Hazard | ⏳=Sand Trap | 💎=Science Target")
    print("Directions: Forward=North(▲) | Back=South(▼) | Left=West(◄) | Right=East(►)")

def parse_telemetry_and_render(packet):
    """Parses incoming coordinates and redraws the UI only on structural updates."""
    global last_x, last_y
    try:
        if "📍 Position:" in packet:
            parts = packet.split("\n")
            pos_line = [line for line in parts if "📍 Position:" in line][0]
            coords = pos_line.split("[")[1].split("]")[0]
            x_val = float(coords.split("X:")[1].split(",")[0].strip())
            y_val = float(coords.split("Y:")[1].strip())
            
            # Wipe and redraw ONLY if the position actually changed
            if x_val != last_x or y_val != last_y:
                last_x, last_y = x_val, y_val
                os.system('cls' if os.name == 'nt' else 'clear')
                print("==========================================================")
                print("🌍 NASA/ESA GROUND OPER
