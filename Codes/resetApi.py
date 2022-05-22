import airsim
import cv2
import numpy as np 
import pprint
import time

client = airsim.CarClient()
client.confirmConnection()

client.enableApiControl(False)