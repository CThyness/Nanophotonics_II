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



def multiple_Images(N_pics, cam_id, f_path, exp_time=0):
    with Vimba.get_instance() as vimba:
         with vimba.get_camera_by_id(cam_id) as cam:
            if(exp_time > 0):
                cam.get_feature_by_name('ExposureTime').set(exp_time)

            for i in range(N_pics): #Takes <N_pictures> images and saves each as a unique .tif file
                            frame = cam.get_frame()
                            f = frame.as_numpy_ndarray()
                            f = f.reshape((768,1024)) #Currently hardcoded the dimensions, should find a way to do this dynamically
                            # avg += f
                            im = Image.fromarray(f)
                            im.save(path.join(f_path, f'{i}.tif'))
                            sleep(0.1)

def full_series(stepper, top_folder, naming_scheme, N_pics, N_secs, cam_id, exp_time, full_dist):
    folder_path = path.join(top_folder, f'{naming_scheme}1a')
    if(not path.exists(folder_path)):
        makedirs(folder_path)
    multiple_Images(N_pics, cam_id, folder_path, exp_time)
    for section in range(2, N_secs+1): #Taking the first run of images with the LED --------------
        stepper.move_by(full_dist//N_secs) #Moving up one section
        stepper.wait_move()
        sleep(1)

        folder_path = path.join(top_folder, f'{naming_scheme}{section}a')
        if(not path.exists(folder_path)):
            makedirs(folder_path)
        multiple_Images(N_pics, cam_id, folder_path)

def full_automation(measurement_folder, top_camera_ID, full_dist, stepper_y, date_folder, N_pictures, N_sections, exposure_time_top_IR, exposure_time_top_LED):
    #Start by ensuring that images taken will be 16bit
    with Vimba.get_instance() as vimba:
        with vimba.get_camera_by_id(top_camera_ID) as cam:
            cam.get_feature_by_name('PixelFormat').set('Mono16')

    #Dark count for LED images -----------------------------------------------------------------------
    folder_path = path.join(measurement_folder, date_folder, f'DarkCount_LED')
    if(not path.exists(folder_path)):
        makedirs(folder_path)
    multiple_Images(N_pictures, top_camera_ID, folder_path, exposure_time_top_LED)
    #-------------------------------------------------------------------------------------------------

    #Dark count for IR images ------------------------------------------------------------------------
    folder_path = path.join(measurement_folder, date_folder, f'DarkCount_IR')
    if(not path.exists(folder_path)):
        makedirs(folder_path)
    multiple_Images(N_pictures, top_camera_ID, folder_path, exposure_time_top_IR)
    #-------------------------------------------------------------------------------------------------

    #Full series of images with LED ------------------------------------------------------------------
    print('Please turn on LED')
    answer = ''
    while(answer != 'y'):
        answer = input('If you have turned on the LED, please type in y: ')

    full_series(stepper_y, path.join(measurement_folder, date_folder), 'top_LED', N_pictures, N_sections, top_camera_ID, exposure_time_top_LED, full_dist)

    #-------------------------------------------------------------------------------------------------

    #Full series of images with IR -------------------------------------------------------------------
    stepper_y.move_by(-full_dist + full_dist//N_sections) #Moving down to the start
    print('Please switch over to IR')
    answer = ''
    while(answer != 'y'):
        answer = input('If you have switched to IR type in y: ')
        
    stepper_y.wait_move()
    sleep(1)

    full_series(stepper_y, path.join(measurement_folder, date_folder), 'top_IR', N_pictures, N_sections, top_camera_ID, exposure_time_top_IR, full_dist)
    #-------------------------------------------------------------------------------------------------

    print('Please switch over to LED')
    answer = ''
    while(answer != 'y'):
        answer = input('If you have switched to LED type in y: ')

    #Taking one more image with LED at the top to estimate drift -------------------------------------
    folder_path = path.join(measurement_folder, date_folder, f'top_LED{N_sections}a_final')
    if(not path.exists(folder_path)):
        makedirs(folder_path)

    multiple_Images(N_pictures, top_camera_ID, folder_path, exposure_time_top_LED)
    #-------------------------------------------------------------------------------------------------

    #Taking one last image with LED at the bottom to estimate drift ----------------------------------
    folder_path = path.join(measurement_folder, date_folder, f'top_LED1a_final')
    if(not path.exists(folder_path)):
        makedirs(folder_path)

    stepper_y.move_by(-full_dist + full_dist//N_sections) #Moving down to the start
    stepper_y.wait_move()
    sleep(1)

    multiple_Images(N_pictures, top_camera_ID, folder_path)
    #-------------------------------------------------------------------------------------------------

def main():
    #Variables NOT to be changed----------------------------------------------------------------------

    #Variables for camera control
    measurement_folder = 'C:/Users/CopsLAB_Local/Documents/CJ_measurements'
    top_camera_ID = 'DEV_0xA4701110AF9B7'
    # front_camera_ID = 'DEV_0xA4701120BE706'
    # exposure_time_front_IR = 500
    # exposure_time_front_LED = 8000

    #Variables for stage movement
    distance_bottom_to_top = 4500000
    stepper_y = tl.KinesisMotor('26004964')
    # stepper_z = tl.KinesisMotor('26004967')
    #-------------------------------------------------------------------------------------------------

    #Variables that need to be changed----------------------------------------------------------------
    date_folder = '230526' #Just insert current date with format YYMMDD
    # images_folder = '1a_IR' #Here write the current measurement being done
    N_pictures = 10 #Number of pictures you want to take
    N_sections = 20 #Number of sections you want to seperate the sample into
    exposure_time_top_IR = 250000
    exposure_time_top_LED = 300
    #-------------------------------------------------------------------------------------------------
    full_automation(measurement_folder, top_camera_ID, distance_bottom_to_top, stepper_y, date_folder, N_pictures, N_sections, exposure_time_top_IR, exposure_time_top_LED)

if(__name__ == "__main__"):
     main()