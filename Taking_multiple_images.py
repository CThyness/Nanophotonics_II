from vimba import Camera, Frame, FrameStatus      # Camera libraries
from vimba import Vimba
from time import sleep
import numpy as np
from PIL import Image #For saving the image
from os import makedirs, path

#Variables NOT to be changed
measurement_folder = 'C:/Users/CopsLAB_Local/Documents/CJ_measurements'
top_camera_ID = 'DEV_0xA4701110AF9B7'
front_camera_ID = 'DEV_0xA4701120BE706'
exposure_time_top_IR = 7000
exposure_time_top_LED = 300
exposure_time_front_IR = 500
exposure_time_front_LED = 8000

#Variables that need to be changed----------------------------------------------------------------
camera_ID = top_camera_ID #The camera you want to use
exposure_time = exposure_time_top_IR #Change to current light source and camera
date_folder = '24.05.23' #Just insert current date (TODO: make this automatic)
images_folder = '1a_IR' #Here write the current measurement being done
N_pictures = 10 #Number of pictures you want to take
#-------------------------------------------------------------------------------------------------

folder_path = path.join(measurement_folder, date_folder, images_folder)
#Check if path exists, if not make all directories required for the full file path to exist
if(not path.exists(folder_path)):
    makedirs(folder_path)

with Vimba.get_instance() as vimba:
    with vimba.get_camera_by_id(camera_ID) as cam:
        
        cam.get_feature_by_name('PixelFormat').set('Mono16')
        cam.get_feature_by_name('ExposureTime').set(exposure_time)
        
        i = 0
        for frame in cam.get_frame_generator(limit=N_pictures): #Takes <N_pictures> images and saves each as a unique .tif file
            f = frame.as_numpy_ndarray()
            f = f.reshape((768,1024)) #Currently hardcoded the dimensions, should find a way to do this dynamically
            im = Image.fromarray(f)
            im.save(path.join(folder_path, f'{i}.tif'))
            i += 1
