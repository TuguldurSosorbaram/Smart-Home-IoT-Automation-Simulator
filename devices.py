class IoTDevice:
    def __init__(self, device_id):
        self.device_id = device_id
        self.status = "off"

    def turn_on(self):
        self.status = "on"

    def turn_off(self):
        self.status = "off"
        
    def toggle(self):
        if self.status == "on":
            self.turn_off()
        else:
            self.turn_on()


class SmartLight(IoTDevice):
    def __init__(self, device_id, brightness=50):
        super().__init__(device_id)
        self.brightness = brightness

    def set_brightness(self, brightness):
        if 0 <= brightness <= 100:
            self.brightness = brightness
        else:
            print("Brightness value should be between 0 and 100.")

    def gradual_dimming(self):
        for level in range(self.brightness, 0, -10):
            print(f"Dimming to {level}%")
            self.set_brightness(level)

    def toggle(self):
        super().toggle()


class Thermostat(IoTDevice):
    def __init__(self, device_id, temperature=20):
        super().__init__(device_id)
        self.temperature = temperature

    def set_temperature(self, temperature):
        if 10 <= temperature <= 30:
            self.temperature = temperature
        else:
            print("Temperature should be between 10°C and 30°C.")

    def set_temperature_range(self, lower_limit, upper_limit):
        self.set_temperature(lower_limit)
        self.set_temperature(upper_limit)

    def toggle(self):
        super().toggle()


class SecurityCamera(IoTDevice):
    def __init__(self, device_id):
        super().__init__(device_id)
        self.motion = False

    def toggleMotion(self):
        if self.motion:
            self.motion = False
        else:
            self.motion = True

    def toggle(self):
        super().toggle()

