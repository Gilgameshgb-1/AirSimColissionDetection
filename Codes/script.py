import airsim
import cv2
import numpy as np 
import pprint
import time

# connect to the AirSim simulator
client = airsim.CarClient()
# client.enableApiControl(True)
client.confirmConnection()

# set camera name and image type to request images and detections
camera_name = "0"
image_type = airsim.ImageType.Scene

# car_controls = airsim.CarControls() # upravljanje autom, inicijalizacija

# set detection radius in [cm]
client.simSetDetectionFilterRadius(camera_name, image_type, 200 * 100) 
# add desired object name to detect in wild card/regex format
client.simAddDetectionFilterMeshName(camera_name, image_type, "Cylinder*") 
client.simAddDetectionFilterMeshName(camera_name, image_type, "Cone*")  #Ova imena asseta ne znam gdje se nalaze nego sam ih iscitao direktno iz simulacije (Pise u sta udaris)
client.simAddDetectionFilterMeshName(camera_name, image_type, "OrangeBall*") 

while True:
    #gps_data = client.getGpsData(gps_name = "Gps", vehicle_name = "mojeAuto") #Uzimamo lat i long sa auta
    #print(gps_data) Ovo radi automatski simDetection API

    distance_sensor_data = client.getDistanceSensorData(distance_sensor_name = "Distance", vehicle_name = "mojeAuto") #distance sensor od neceg

    rawImage = client.simGetImage(camera_name, image_type)
    if not rawImage:
        continue
    png = cv2.imdecode(airsim.string_to_uint8_array(rawImage), cv2.IMREAD_UNCHANGED)
    objects = client.simGetDetections(camera_name, image_type)
    if objects:
        for object in objects:
            # s = pprint.pformat(object) Lijepi format ispisivanja atributa objekta
            print("Ime objekta: %s" % object.name) #printa nam ime objekta
            # print("Pos: %s" % object.relative_pose.position) #prava pozicija
            # print("relPos: %s" % object.relative_pose.orientation.w_val) #dubina
            # print("XDistRel: %s" % object.relative_pose.orientation.x_val) #rel x vrijednost
            # print("YDistRel: %s" % object.relative_pose.orientation.y_val) #rel x vrijednost

            print("Udaljenost: %s" % distance_sensor_data) # na osnovu ovog bi mogli zakociti auto recimo distance ispod 10 palimo kocenje

            #-----------------------------------Testiranje voznje -----------------------------------
            # car_controls.throttle = 1
            # client.setCarControls(car_controls)
            # time.sleep(3)

            # car_controls.throttle = 0
            # car_controls.brake = 1
            # client.setCarControls(car_controls)

            # time.sleep(3)

            # car_controls.brake = 0
            # car_controls.throttle = 1 #vozi desno
            # car_controls.steering = 1
            # client.setCarControls(car_controls)

            # time.sleep(3)

            # car_controls.throttle = 1
            # car_controls.steering = -1 #vozi lijevo
            # client.setCarControls(car_controls)

            # time.sleep(3)
            # car_controls.brake = 1
            # client.setCarControls(car_controls)
            #Imace efekat hodanja po cesti
            #-----------------------------------Testiranje voznje -----------------------------------
            #Na osnovu distance-a bi mogli ubacivati kontrole na auto
            #Napraviti prvo da zaobidje jedan objekat pa onda ici dalje na komplikovanije situacije
            #cv2 fakticki trenutno nema nikakvu svrhu
            cv2.rectangle(png,(int(object.box2D.min.x_val),int(object.box2D.min.y_val)),(int(object.box2D.max.x_val),int(object.box2D.max.y_val)),(255,0,0),2)
            cv2.putText(png, object.name, (int(object.box2D.min.x_val),int(object.box2D.min.y_val - 10)), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (36,255,12))

    
    cv2.imshow("AirSim", png)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    elif cv2.waitKey(1) & 0xFF == ord('c'):
        client.simClearDetectionMeshNames(camera_name, image_type)
    elif cv2.waitKey(1) & 0xFF == ord('a'):
        client.simAddDetectionFilterMeshName(camera_name, image_type, "Cylinder*")
cv2.destroyAllWindows() 