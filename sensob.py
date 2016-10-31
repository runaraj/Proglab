class sensob:
    sensors = [] #One or more of the sensors associated with this class
    sensor_values = [] #values associated with the sensors

    def update(self): #force the sensob to fetch the relevant sensor value(s) and convert them into the pre-processed sensob value
        self.sensor_values.clear()
        for sensor in self.sensors:
            self.sensor_values.append(sensor.update)

    def get_values(self):
        return self.sensor_values


    def set_sensors(self, newSensors):
        for sens in newSensors:
            self.sensors.append(sens)