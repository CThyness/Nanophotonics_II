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
# exposure_time_front_IR = 500
# exposure_time_front_LED = 8000

#Variables for stage movement
distance_bottom_to_top = 4000000
serial_y = '26004964'
# serial_z = '26004967'
stepper_y = tl.KinesisMotor(serial_y)
# stepper_z = tl.KinesisMotor(serial_z)
#-------------------------------------------------------------------------------------------------

#Variables that need to be changed----------------------------------------------------------------
date_folder = '25.05.23' #Just insert current date (TODO: make this automatic)
# images_folder = '1a_IR' #Here write the current measurement being done
N_pictures = 10 #Number of pictures you want to take
N_sections = 20 #Number of sections you want to seperate the sample into
exposure_time_top_IR = 250000
exposure_time_top_LED = 300
#-------------------------------------------------------------------------------------------------

#Check if path exists, if not make all directories required for the full file path to exist
# do:
#     print('Move the camera to the bottom.')
#     print('Write x followed by number ')y

with Vimba.get_instance() as vimba:
        with vimba.get_camera_by_id(top_camera_ID) as cam:
            cam.get_feature_by_name('PixelFormat').set('Mono16')

            #Dark count for LED images -----------------------------------------------------------
            cam.get_feature_by_name('ExposureTime').set(exposure_time_top_LED)
            folder_path = path.join(measurement_folder, date_folder, f'DarkCount_LED')
            if(not path.exists(folder_path)):
                makedirs(folder_path)
            for i in range(N_pictures): #Takes <N_pictures> images and saves each as a unique .tif file
                    frame = cam.get_frame()
                    f = frame.as_numpy_ndarray()
                    f = f.reshape((768,1024)) #Currently hardcoded the dimensions, should find a way to do this dynamically
                    # avg += f
                    im = Image.fromarray(f)
                    im.save(path.join(folder_path, f'{i}.tif'))
                    sleep(0.1)
            #-------------------------------------------------------------------------------------

            #Dark count for IR images ------------------------------------------------------------
            cam.get_feature_by_name('ExposureTime').set(exposure_time_top_IR)
            folder_path = path.join(measurement_folder, date_folder, f'DarkCount_IR')
            if(not path.exists(folder_path)):
                makedirs(folder_path)
            for i in range(N_pictures): #Takes <N_pictures> images and saves each as a unique .tif file
                    frame = cam.get_frame()
                    f = frame.as_numpy_ndarray()
                    f = f.reshape((768,1024)) #Currently hardcoded the dimensions, should find a way to do this dynamically
                    # avg += f
                    im = Image.fromarray(f)
                    im.save(path.join(folder_path, f'{i}.tif'))
                    sleep(0.1)
            #-------------------------------------------------------------------------------------

            cam.get_feature_by_name('ExposureTime').set(exposure_time_top_LED)
            print('Please turn on LED')
            answer = ''
            while(answer != 'y'):
                answer = input('If you have turned on the LED, please type in y: ')

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
                stepper_y.wait_move()
                sleep(1)
            #-------------------------------------------------------------------------------------
            tl.KinesisMotor.move_by(stepper_y, -distance_bottom_to_top)
            print('Please switch over to IR')
            answer = ''
            while(answer != 'y'):
                answer = input('If you have switched to IR type in y: ')
                
            stepper_y.wait_move()
            sleep(1)
            for section in range(1, N_sections+1): #Taking all images with IR --------------------

                folder_path = path.join(measurement_folder, date_folder, f'top_IR{section}a')
                if(not path.exists(folder_path)):
                    makedirs(folder_path)

                cam.get_feature_by_name('ExposureTime').set(exposure_time_top_IR)

                # avg = np.zeros((768,1024), np.float64)
                for i in range(N_pictures): #Takes <N_pictures> images and saves each as a unique .tif file
                    frame = cam.get_frame()
                    f = frame.as_numpy_ndarray()
                    f = f.reshape((768,1024)) #Currently hardcoded the dimensions, should find a way to do this dynamically
                    # avg += f
                    im = Image.fromarray(f)
                    im.save(path.join(folder_path, f'{i}.tif'))
                    sleep(exposure_time_top_IR + 0.1) #To ensure that there is always enough sleep time between pictures
                tl.KinesisMotor.move_by(stepper_y, distance_bottom_to_top//N_sections) #Moving down one section
                stepper_y.wait_move()
                sleep(1)
            #     avg = avg/N_pictures
            #     im = Image.fromarray(avg)
            #     im.save(path.join(folder_path, 'avg.tif'))
            #-------------------------------------------------------------------------------------
            cam.get_feature_by_name('ExposureTime').set(exposure_time_top_LED)
            print('Please switch over to LED')
            answer = ''
            while(answer != 'y'):
                answer = input('If you have switched to LED type in y: ')

            #Taking one more image with LED at the top to estimate drift -------------------------
            folder_path = path.join(measurement_folder, date_folder, f'top_LED{N_sections}a_final')
            if(not path.exists(folder_path)):
                makedirs(folder_path)
            
            tl.KinesisMotor.move_by(stepper_y, -distance_bottom_to_top//N_sections) #Moving down one section
            stepper_y.wait_move()
            sleep(1)

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
            #Taking one last image with LED at the bottom to estimate drift ----------------------
            folder_path = path.join(measurement_folder, date_folder, f'top_LED1a_final')
            if(not path.exists(folder_path)):
                makedirs(folder_path)
            tl.KinesisMotor.move_by(stepper_y, -distance_bottom_to_top) #Moving down to the start
            stepper_y.wait_move()
            sleep(1)

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
            

