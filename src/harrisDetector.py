#!/usr/bin/python3

from display import Display
import sys
import getopt
import cv2
import numpy as np









if __name__ == "__main__":
    display_image = False
    display_video = False

    W, H = 800, 600

    disp = Display(W,H)

    try:
        opts,args = getopt.getopt(sys.argv[1:],'i:v',['img=','vid='])
    except getopt.GetoptError:
        print("harrisDetector.py --img=<image directory path> OR -vid=<mp4 path>")
        sys.exit(2)
    for opt,arg in opts:
        if opt in ('-i','--img'):
            img_path = arg
            if(not img_path):
                print("no image path specified")
                sys.exit()
            display_image = True
            break
        elif opt in ('-v','--vid'):
            vid_path = arg
            if(not vid_path):
                print("no video path specified")
                sys.exit()
            display_video = True
            break

    #render image
    if(display_image):
        #get image
        img = cv2.imread(img_path)
        img = cv2.resize(img, dsize=(W,H))

        #display loop
        while True:
            disp.checkExit()
            #display image
            disp.paint(img)


    #render video
    if(display_video):
        #get stream and resize
        cap = cv2.VideoCapture(vid_path)
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, W)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, H)


        #invalid stream
        if(cap.isOpened()==False):
            print("error reading .mp4")
            sys.exit()

        #display loop
        while True:
            disp.checkExit()

            #extract frame and display
            ret, frame = cap.read()
            if ret == True:
                disp.paint(frame)



