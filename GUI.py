import threading
import tkinter as tk
from tkinter import ttk
from functools import partial
from datetime import datetime


from CentralAutomationSystem import AutomationSystem, automation_loop
from devices import SecurityCamera, SmartLight, Thermostat


class AutomationGUI:
    def __init__(self, automation_system):
        self.automation_system = automation_system

        self.root = tk.Tk()
        self.root.title("Automation System GUI")

        self.create_widgets()
        self.update_gui("Log for IoT devices:")
        self.automation_thread = threading.Thread(target=automation_loop, args=(automation_system,))
        self.automation_thread.start()

        self.root.after(2000, self.update_gui_periodic)

    def create_widgets(self):
        # TOGGLEAUTOMATION
        self.toggle_automation_button = tk.Button(self.root, text="Toggle Automation", command=self.toggle_automation)
        self.toggle_automation_button.pack()

        # AUTOMATIONSTATUS
        self.automation_status_label = tk.Label(self.root, text="Automation Status: ")
        self.automation_status_label.pack()

        # STATUS
        self.status_text = tk.Text(self.root, height=5, width=70)
        self.status_text.tag_configure("center", justify='center')
        self.status_text.pack()

        # CONTROLS
        for device in self.automation_system.devices:
            self.add_device_control(device)

        # LOG
        self.log_text = tk.Text(self.root, height=10, width=70)
        self.log_text.pack()

    def add_device_control(self, device):
        control_frame = tk.Frame(self.root)
        control_frame.pack()

        device_status_label = tk.Label(control_frame, text=f"{device.device_id}")
        device_status_label.pack()

        if isinstance(device, SmartLight):
            brightness_label = tk.Label(control_frame, text="Current Brightness: 0%")
            brightness_label.pack()

            # lower limit
            lower_limit_label = tk.Label(control_frame, text="0")
            lower_limit_label.pack(side=tk.LEFT)
            brightness_scale = ttk.Scale(control_frame, from_=0, to=100, orient=tk.HORIZONTAL)
            brightness_scale.pack(side=tk.LEFT)
            # Higher limit label
            higher_limit_label = tk.Label(control_frame, text="100")
            higher_limit_label.pack(side=tk.LEFT)

            toggle_button = tk.Button(control_frame, text="Toggle", command=partial(self.toggle_device, device))
            toggle_button.pack()

            brightness_scale.bind("<ButtonRelease-1>", lambda event, device=device: self.update_after_release(event, device,brightness_label))

        elif isinstance(device, Thermostat):
            temperature_label = tk.Label(control_frame, text="Current Temperature: 0C")
            temperature_label.pack()

            # Lower limit label
            lower_limit_label = tk.Label(control_frame, text="10")
            lower_limit_label.pack(side=tk.LEFT)
            temperature_scale = ttk.Scale(control_frame, from_=10, to=30, orient=tk.HORIZONTAL)
            temperature_scale.pack(side=tk.LEFT)
            # Higher limit label
            higher_limit_label = tk.Label(control_frame, text="30")
            higher_limit_label.pack(side=tk.LEFT)

            temperature_scale.bind("<ButtonRelease-1>", lambda event, device=device: self.update_after_release(event, device, temperature_label))

            toggle_button = tk.Button(control_frame, text="Toggle", command=partial(self.toggle_device, device))
            toggle_button.pack()

        elif isinstance(device, SecurityCamera):
            toggle_button = tk.Button(control_frame, text="Toggle Security", command=partial(self.toggle_device, device))
            toggle_button.pack()

    def update_after_release(self, event, device,label):
        value = event.widget.get()
        if isinstance(device, SmartLight):
            self.change_brightness(device, value)
            label.config(text=f"Current Brightness: {int(value)}%")
        elif isinstance(device, Thermostat):
            self.change_temperature(device, value)
            label.config(text=f"Current Temperature: {int(value)}C")
    
    def toggle_automation(self):
        self.automation_system.toggle_automation(not self.automation_system.automation_enabled)
        log_entry = f"{datetime.now()}: Automation {'On' if self.automation_system.automation_enabled else 'Off'}"
        self.update_gui(log_entry)

    def toggle_device(self, device):
        device.toggle()
        log_entry = f"{datetime.now()}: {device.device_id} {device.status}"
        self.update_gui(log_entry)

    def change_brightness(self, device, value):
        device.set_brightness(int(float(value)))
        log_entry = f"{datetime.now()}: Brightness changed to {device.brightness}"
        self.update_gui(log_entry)

    def change_temperature(self, device, value):
        device.set_temperature(int(float(value)))
        log_entry = f"{datetime.now()}: Temperature changed to {device.temperature}"
        self.update_gui(log_entry)

    def update_gui_periodic(self):
        # Update the GUI here
        self.update_gui("")
        
        # Schedule the next update
        self.root.after(2000, self.update_gui_periodic)

    def update_gui(self,log_entry):
        if(log_entry == ""):
            self.automation_status_label.config(text=f"Automation Status: {'On' if self.automation_system.automation_enabled else 'Off'}")
            status_text = "\n".join([f"{device.device_id} Status: {device.status}" for device in self.automation_system.devices])
            self.status_text.delete("1.0","end")
            self.status_text.insert(tk.END, status_text + "\n",'center')
            automation_system.save_sensor_data_to_file()
        else:
            #AUTOMATIONSTATUS
            self.automation_status_label.config(text=f"Automation Status: {'On' if self.automation_system.automation_enabled else 'Off'}")

            # STATUS
            status_text = "\n".join([f"{device.device_id} Status: {device.status}" for device in self.automation_system.devices])
            self.status_text.delete("1.0","end")
            self.status_text.insert(tk.END, status_text + "\n",'center')


            # LOG
            self.log_text.insert(tk.END, log_entry + "\n")
            self.automation_system.sensor_data.append(log_entry)
            self.log_text.yview(tk.END)  # Auto-scroll to the bottom of the log

            # get data for file
            automation_system.save_sensor_data_to_file()

# Example Usage
automation_system = AutomationSystem()

# Add devices to the system
light1 = SmartLight(device_id="Living Room light")
thermostat1 = Thermostat(device_id="Living Room Temperature")
camera1 = SecurityCamera(device_id="Front Door Security Camera")

automation_system.add_device(light1)
automation_system.add_device(thermostat1)
automation_system.add_device(camera1)

# Create GUI for the automation system
gui = AutomationGUI(automation_system)

# Run the GUI main loop
gui.root.mainloop()
gui.automation_system.stop_event.set()
gui.automation_thread.join()