import cv2 #Highly overkill I think
from vimba import *
from time import sleep
import numpy as np
from PIL import Image 

def take_image(cam_id, f_name): #Takes a singular picture with chosen camera and saves it as "<f_name>.jpg"
    with vimba.get_camera_by_id(cam_id) as cam:
        frame = cam.get_frame()
        frame.convert_pixel_format(PixelFormat.Mono8) #This sets the camera to use Mono8 (8-bit image [monochrome?])
        cv2.imwrite (f'{f_name}.jpg ', frame.as_opencv_image()) #Just a ludacrious way of storing the image? Seems like it
        #Ok, now lets assume this then just saves an image as a jpg

def find_exposure_time(initial_guess, cam_id): #Figures out the optimal exposure time, sets the camera to it and returns it
    exposure_time = initial_guess
    max_pixel = 256 #Just an initial value to make the while loop start
    img_name = 'for_exp_time'
    print('start')
    with vimba.get_camera_by_id(cam_id) as cam:
        increment = cam.ExposureTime.get_increment()
        while(np.abs(max_pixel-230) > 20): #Somewhat quick changes to get a fairly good exposure time
            if(max_pixel < 230): exposure_time = exposure_time + ((exposure_time*0.1)//increment)*increment #Increases exposure time ~10% but ensures that it is done in a whole number of increments
            elif(max_pixel > 230): exposure_time = exposure_time - ((exposure_time*0.1)//increment)*increment #Same as above, just lowering this time
            cam.ExposureTime.set(exposure_time)
            take_image(cam_id, img_name)
            pixel_values = np.asarray(Image.open(f'{img_name}.jpg'))
            max_pixel = np.max(pixel_values)
        print(f'rough time found: {exposure_time}')

        if(max_pixel < 230): #Slow and incremental changes to exposure time, so we can find the optimal one
            tmp_max_pixel = max_pixel + 1
            while(tmp_max_pixel > max_pixel and tmp_max_pixel <= 230):
                exposure_time += 1
                cam.ExposureTime.set(exposure_time)
                take_image(cam_id, img_name)
                pixel_values = np.asarray(Image.open(f'{img_name}.jpg'))
                max_pixel = np.max(pixel_values)
            exposure_time -= 1
        elif(max_pixel > 230):
            tmp_max_pixel = max_pixel - 1
            while(max_pixel > 230 and tmp_max_pixel >= 230):
                exposure_time -= 1
                cam.ExposureTime.set(exposure_time)
                take_image(cam_id, img_name)
                pixel_values = np.asarray(Image.open(f'{img_name}.jpg'))
                max_pixel = np.max(pixel_values)
            exposure_time += 1
        print(f'Optimal time found: {exposure_time}')
        cam.ExposureTime.set(exposure_time)
    return(exposure_time)


def main():
    with Vimba.get_instance() as vimba:
        front_camera_id =  'djlefakjlkjd' #The IDs are just placeholders as I do not know the actual IDs
        top_camera_id =  'klajsflsaj'

        for i in range(10): #just to check that nothing fucked happens (within a minute at least).
            print(f'test {i}: front camera is {front_camera} and top camera is {top_camera}')
            sleep(6)
        take_image(front_camera, 'test') #Takes a test image with the front camera

if __name__ == '__main__':
    main()
