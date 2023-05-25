#General libraries
from time import sleep
import numpy as np
from PIL import Image #For saving the image
from os import makedirs,path

#Camera control libraries
from vimba import Camera, Frame, FrameStatus
from vimba import Vimba

#Stage control libraries
import ft232
from pylablib.devices import Thorlabs as tl

#Variables NOT to be changed----------------------------------------------------------------------

#Variables for camera control
measurement_folder = 'C:/Users/CopsLAB_Local/Documents/CJ_measurements'
top_camera_ID = 'DEV_0xA4701110AF9B7'
# front_camera_ID = 'DEV_0xA4701120BE706'
exposure_time_top_IR = 7000
exposure_time_top_LED = 300
# exposure_time_front_IR = 500
# exposure_time_front_LED = 8000

#Variables for stage movement
distance_bottom_to_top = 3500000
serial_y = '26004964'
# serial_z = '26004967'
stepper_y = tl.KinesisMotor(serial_y)
# stepper_z = tl.KinesisMotor(serial_z)
#-------------------------------------------------------------------------------------------------

#Variables that need to be changed----------------------------------------------------------------
date_folder = '25.05.23_test' #Just insert current date (TODO: make this automatic)
# images_folder = '1a_IR' #Here write the current measurement being done
N_pictures = 10 #Number of pictures you want to take
N_sections = 10 #Number of sections you want to seperate the sample into
#-------------------------------------------------------------------------------------------------

#Check if path exists, if not make all directories required for the full file path to exist
# do:
#     print('Move the camera to the bottom.')
#     print('Write x followed by number ')

with Vimba.get_instance() as vimba:
        with vimba.get_camera_by_id(top_camera_ID) as cam:
            cam.get_feature_by_name('PixelFormat').set('Mono16')
            cam.get_feature_by_name('ExposureTime').set(exposure_time_top_LED)
            for section in range(1, N_sections+1): #Taking the first run of images with the LED --
                folder_path = path.join(measurement_folder, date_folder, f'top_LED{section}a')
                if(not path.exists(folder_path)):
                    makedirs(folder_path)
                
                # avg = np.zeros((768,1024), np.float64)
                for i in range(N_pictures): #Takes <N_pictures> images and saves each as a unique .tif file
                    frame = cam.get_frame()
                    f = frame.as_numpy_ndarray()
                    f = f.reshape((768,1024)) #Currently hardcoded the dimensions, should find a way to do this dynamically
                    # avg += f
                    im = Image.fromarray(f)
                    im.save(path.join(folder_path, f'{i}.tif'))
                    sleep(0.1)
                # avg = avg//N_pictures
                # im = Image.fromarray(avg)
                # im.save(path.join(folder_path, 'avg.tif'))

                tl.KinesisMotor.move_by(stepper_y, distance_bottom_to_top//N_sections) #Moving up one section
                sleep(2)
            #-------------------------------------------------------------------------------------
            print('Please switch over to IR')
            answer = ''
            while(answer != 'y'):
                answer = input('If you have switched to IR type in y: ')
                
            tl.KinesisMotor.move_by(-distance_bottom_to_top)
            for section in range(1, N_sections+1): #Taking all images with IR ----------------------
                tl.KinesisMotor.move_by(stepper_y, distance_bottom_to_top//N_sections) #Moving down one section
                sleep(2)

                folder_path = path.join(measurement_folder, date_folder, f'top_IR{section}a')
                if(not path.exists(folder_path)):
                    makedirs(folder_path)

                # avg = np.zeros((768,1024), np.float64)
                for i in range(N_pictures): #Takes <N_pictures> images and saves each as a unique .tif file
                    frame = cam.get_frame()
                    f = frame.as_numpy_ndarray()
                    f = f.reshape((768,1024)) #Currently hardcoded the dimensions, should find a way to do this dynamically
                    # avg += f
                    im = Image.fromarray(f)
                    im.save(path.join(folder_path, f'{i}.tif'))
                    sleep(0.1)
            #     avg = avg/N_pictures
            #     im = Image.fromarray(avg)
            #     im.save(path.join(folder_path, 'avg.tif'))
            #-------------------------------------------------------------------------------------
            print('Please switch over to LED')
            answer = ''
            while(answer != 'y'):
                answer = input('If you have switched to LED type in y: ')

            #Taking one last image with LED to estimate drift ------------------------------------
            folder_path = path.join(measurement_folder, date_folder, f'top_LED{N_sections}a_final')
            if(not path.exists(folder_path)):
                makedirs(folder_path)

            # avg = np.zeros((768,1024), np.float64)
            for i in range(N_pictures): #Takes <N_pictures> images and saves each as a unique .tif file
                frame = cam.get_frame()
                f = frame.as_numpy_ndarray()
                f = f.reshape((768,1024)) #Currently hardcoded the dimensions, should find a way to do this dynamically
                # avg += f
                im = Image.fromarray(f)
                im.save(path.join(folder_path, f'{i}.tif'))
                sleep(0.1)
            # avg = avg/N_pictures
            # im = Image.fromarray(avg)
            # im.save(path.join(folder_path, 'avg.tif'))
            #-------------------------------------------------------------------------------------

