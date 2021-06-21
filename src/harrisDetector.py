#!/usr/bin/python3

from display import Display
from detector import Detector
from stitcher import Stitcher
import sys
import getopt
import cv2
import numpy as np
import time
import os
import glob


if __name__ == "__main__":
    display_image = False
    display_video = False
    display_stitch = False

    W, H = 400, 300

    disp = Display(W,H)
    detect = Detector(W,H,10,0.2)
    stitcher = Stitcher()




    try:
        opts,args = getopt.getopt(sys.argv[1:],'i:vd',['img=','vid=','dir='])
    except getopt.GetoptError:
        print("harrisDetector.py --img=<image directory path> OR --vid=<mp4 path> OR --dir=<directory of images>")
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
        elif opt in ('-d', '--dir'):
            dir_path = arg
            if(not dir_path):
                print("no directory specified")
                sys.exit()
            display_stitch = True
            break

    #render stitching
    if(display_stitch):

        filenames = glob.glob(dir_path+"/*.jpg")
        filenames.sort()
        images = [cv2.imread(img) for img in filenames]
        for image in images:
            #resize
            image = cv2.resize(image, dsize=(W,H))
            #grayscale img
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

            detect.set_image(gray)
            detect.find_interest_points()
            stitcher.load_image(detect.get_image(),detect.get_rMap())
        print("WARNING stitching does not work, the computed homographies do not correctly stitch images together. this script will show the individual images with their incorrect projections")
        stitcher.stitch()




    #render image
    if(display_image):
        #get image
        image = cv2.imread(img_path)
     #   image = np.uint8(image)
        image = cv2.resize(image, dsize=(W,H))

        #grayscale img
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        detect.set_image(gray)
        detect.smooth_img()

        smooth = detect.get_image()

        detect.find_interest_points()
        lamda = detect.get_lamdaF()
        img = detect.get_image()
        rMap = detect.get_rMap()

        #display loop
        while True:
            disp.checkInput()
            #display image
            disp.paint(image,smooth,img,rMap,lamda[:,:,0],lamda[:,:,1])






    #render video
    if(display_video):
        #get stream and resize
        cap = cv2.VideoCapture(vid_path)
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, W)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, H)
        out = cv2.VideoWriter('output.avi',
                              cv2.VideoWriter_fourcc('M','P','E','G'),10,(
                                  int(cap.get( cv2.CAP_PROP_FRAME_WIDTH)),
                                  int(cap.get( cv2.CAP_PROP_FRAME_HEIGHT))))

        if(cap.isOpened()==False):
            print("error reading .mp4")
            sys.exit()

        #generate data loop
        imgs = []
        points = []
        count = 0
        print("video preprocesses data... this may take a while")
        while count < 300 or not cap.isOpened():
            ret, frame = cap.read()
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            detect.set_image(gray)
            detect.find_interest_points()
            imgs.append(detect.get_image())
            print(imgs[count].shape)
            p = detect.get_points()
            points.append(len(p))
            for pnts in p:
                cv2.circle(gray,pnts,4, (0,0,255), -1)

            print("img {} of 300 proccessed".format(count))
            outim = cv2.cvtColor(gray,cv2.COLOR_GRAY2BGR)
            out.write(outim)
            count+=1

        cap.release()
        out.release()
        for i in range(len(imgs)):
            disp.paint_vid(imgs[i],points[i])
            time.sleep(0.1667)


