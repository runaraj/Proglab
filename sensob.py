from ultrasonic import Ultrasonic
from camera import Camera
import imager2 as Imager
from reflectance_sensors import ReflectanceSensors
from irproximity_sensor import IRProximitySensor

class Sensob:
    sensors = [] #One or more of the sensors associated with this class
    sensor_values = [] #values associated with the sensors

    def __str__(self):
        ors = "Sensors: ", self.sensors
        val = "Values: ", self.sensor_values
        return ors + "\n" + val

    def update(self): #force the sensob to fetch the relevant sensor value(s) and convert them into the pre-processed sensob value
        self.sensor_values.clear()
        for sensor in self.sensors:
            sensor.update()
            self.sensor_values.append(sensor.get_value())
        print("Verdier i sensob:", self.sensor_values)

    def get_values(self):
        if len(self.sensors) == 0:
            raise Exception("No sensors")
        elif len(self.sensor_values) == 0:
            self.update()
        return self.sensor_values


    def set_sensors(self, newSensors):
        for sens in newSensors:
            self.sensors.append(sens)
        self.update()

    def reset_sensors(self):
        for sens in self.sensors:
            sens.reset()
        self.sensor_values.clear()
