import airsim
import cv2
import numpy as np 
import pprint
import time

client = airsim.CarClient()
client.confirmConnection()

client.enableApiControl(True)
car_controls = airsim.CarControls()
car_controls.is_manual_gear = True

#incijalizacija kamere
camera_name = "0"
image_type = airsim.ImageType.Scene

#detection radius u centimetrima i objekti koje prihvatamo da smo detektovali
client.simSetDetectionFilterRadius(camera_name, image_type, 200 * 100) 
client.simAddDetectionFilterMeshName(camera_name, image_type, "Cylinder*") 
client.simAddDetectionFilterMeshName(camera_name, image_type, "Cone*")  
client.simAddDetectionFilterMeshName(camera_name, image_type, "OrangeBall*") 

while True:

    rawImage = client.simGetImage(camera_name, image_type)
    if not rawImage:
        continue
    png = cv2.imdecode(airsim.string_to_uint8_array(rawImage), cv2.IMREAD_UNCHANGED)
    objects = client.simGetDetections(camera_name, image_type)
    if objects:
        for object in objects:
            print("Objekat: %s" % object) 

    data_car = client.getDistanceSensorData(vehicle_name="mojeAuto")
    state_car = client.getCarState()
    print(f"Car speed: {state_car.speed}")
    print(f"Distance sensor data: Car1: {data_car.distance}")
    if data_car.distance > 15:
        car_controls.manual_gear = 1
        car_controls.throttle = 0.3
        client.setCarControls(car_controls)
    if data_car.distance <= 15:
        car_controls.brake = 1
        car_controls.throttle = 0
        client.setCarControls(car_controls)
        if(state_car.speed <= 0.5):
            time.sleep(2)
    if state_car.speed == 0:
        car_controls.brake = 0
        car_controls.manual_gear = -1
        car_controls.throttle = -1
        client.setCarControls(car_controls)
        time.sleep(3)
#Opis koda, auto ide pravo, na 15 metara udaljenosti stane
#krene u rikverc i ponavlja to