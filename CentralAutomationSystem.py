import random
import json
from datetime import datetime
import threading
import time
from devices import SecurityCamera, SmartLight, Thermostat

class AutomationSystem:
    def __init__(self):
        self.devices = []
        self.sensor_data = []
        self.lock = threading.Lock()
        self.stop_event = threading.Event()
        self.automation_enabled = True  

    def toggle_automation(self, enable=True):
        self.automation_enabled = enable
        print(f"Automation {'enabled' if enable else 'disabled'}.")

    def discover_device(self, device):
        with self.lock:
            self.devices.append(device)
            print(f"Discovered new device: {device.device_id}")

    def add_device(self, device):
        with self.lock:
            if device not in self.devices:
                self.devices.append(device)
                print(f"Added device: {device.device_id} to the system.")
            else:
                print(f"Device {device.device_id} is already in the system.")

    def simulate_randomization(self):
        for device in self.devices:
            with self.lock:
                if isinstance(device, SecurityCamera) and device.status == "on":
                    if random.choice([True, False]):
                        device.toggleMotion()
                        if(device.motion):
                            print(f"New Motion detected on {device.device_id}")
                            self.sensor_data.append(f"New Motion detected on {device.device_id}\nLights are turned on")
                        else:
                            print(f"Motion removed on {device.device_id}")
                            self.sensor_data.append(f"Motion removed on {device.device_id}")
                    if device.motion:
                        for d in self.devices:
                            if isinstance(d, SmartLight) and d.status == "off":
                                d.status = "on"


    def save_sensor_data_to_file(self, filename="sensor_data.json"):
        with self.lock:
            with open(filename, "w") as file:
                json.dump(self.sensor_data, file, indent=4)


def automation_loop(system, interval=5):
    while not system.stop_event.is_set():
        time.sleep(interval)
        if system.automation_enabled:  # Check if automation is enabled
            system.simulate_randomization()


