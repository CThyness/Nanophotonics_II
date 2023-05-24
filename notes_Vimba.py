# -*- coding: utf-8 -*-
"""
Created on Wed May 24 13:38:47 2023

@author: COPS
"""

# Camera
from vimba import Camera, Frame, FrameStatus      # Camera libraries
from vimba import Vimba
from time import sleep
import numpy as np
from PIL import Image

framQueue = []

def frame_handler(cam: Camera, frame: Frame):

    # Set global frame obtained from camera
    global frameQ
    global framQueue
        
    while frame.get_status() != FrameStatus.Complete:
        time.sleep(0.01)
        
    frameQ = frame.as_numpy_ndarray()
    
    
    # Set frame to CAMERA queue
    cam.queue_frame(frame)
    framQueue.append(frameQ)
    
    # Define variables as self?
    cam = cam

# Open Vimba CCD environment
with Vimba.get_instance() as vimb:
    with vimb.get_all_cameras()[0] as cameraWS:
        
        cameraWS.get_feature_by_name('PixelFormat').set('Mono16')
        
        # # Set camera properties WS
        # cameraWS.get_feature_by_name('Height').set()
        # cameraWS.get_feature_by_name('Width').set()
        # cameraWS.get_feature_by_name('OffsetX').set()
        # cameraWS.get_feature_by_name('OffsetY').set()
        # cameraWS.get_feature_by_name('ExposureTime').set()
        # cameraWS.get_feature_by_name('PixelFormat').set()
        
        # Pause for camera
        sleep(1)
        
        # cameraWS.start_streaming(handler=frame_handler, buffer_count=10)
        for frame in cameraWS.get_frame_generator(limit=10): #Takes 10 images and saves each as a .tiff file
            f = frame.as_numpy_ndarray()
            f = f.reshape((768,1024))
            im = Image.fromarray(f)
            im.save('test.tif')


        # Pause for camera
        sleep(0.3)
        
        # # a = cameraWS.queue_frame()
        # pic1 = frameQ
        
        # res = pic1.shape
        # imgs = np.zeros(res[:-1])
        
        # # Iterate over index
        # for k1 in range(res[0]):
        #     for k2 in range(res[1]):
        #         imgs[k1][k2] = pic1[k1][k2][0]
        
        