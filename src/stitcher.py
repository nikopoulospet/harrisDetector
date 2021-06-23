import numpy as np
import cv2
import heapq
import random
import math
import sys

class Stitcher:
    def __init__(self):
        """
        Stiching class, stitches images together using computed descriptors from
        the detector class.
        Currently this class utilizes many algorithms from the opencv library in
        the future these will be broken apart and implimented from scratch
        """
        self.epsilon = 100
        self.SSDthresh = 1000
        self.descriptorCutoff = 1000 # needed because of overflow with large nums
        self.list_of_pairs = []
        self.list_of_differences = []
        self.__images = []
        self.__descriptors = []
        self.__keypoints = []
        self.__SSDmap = {}

    def load_image(self, image, descriptor):
        self.__images.append(image)
        Karr = []
        Darr = []
        for x in range(descriptor[0,:].size):
            for y in range(descriptor[:,0].size):
                if(descriptor[y][x] != 0):
                    Karr.append([x,y,1])
                    Darr.append(descriptor[y][x]//self.descriptorCutoff)

        #splice descriptor to get keypoints and descriptors of each kp
        self.__descriptors.append(Darr)
        self.__keypoints.append(Karr)
        if(len(self.__descriptors) > 1):
            print(len(self.__descriptors[1]))
            print(len(self.__keypoints[1]))

    def stitch(self):
        if(len(self.__images) < 2):
            print("please load images")
            return

        for im1 in range(0,len(self.__images)):
            im2 = im1+1
            if(im2 >= len(self.__images)):
                im2 = 0

            self.outlier_rejection(im1,im2)

            h = self.RANSAC(len(self.list_of_pairs)//4)

            print("computed H for img no: {} and img no: {}".format(im1,im2))
            print(h)

            im_out = cv2.warpPerspective(self.__images[im1], h, (self.__images[im2].shape[1],self.__images[im2].shape[0]))
            cv2.imshow("Source Image no: {}".format(im1), self.__images[im1])
            cv2.imshow("Destination Image no: {}".format(im2), self.__images[im2])
            cv2.imshow("Warped Source Image no: {}:{}".format(im1,im2), im_out)

        cv2.waitKey(0)



    def outlier_rejection(self, im1, im2):
        for indx1 in range(len(self.__descriptors[im1])):
            for indx2 in range(len(self.__descriptors[im2])):

                #get discs out of array based on index
                desc1 = self.__descriptors[im1][indx1]
                desc2 = self.__descriptors[im2][indx2]

                #calcualte difference between descriptor intensities, should be SSD
                temp = self.dist(desc1,desc2)
                #print(indx1,indx2,temp)
                if (temp < self.SSDthresh):
                    self.list_of_pairs.append((self.__keypoints[im1][indx1], self.__keypoints[im2][indx2]))

        #print(len(self.list_of_pairs))


    def RANSAC(self, numLoops):
        """
        taking the best 4 matches in the computed heap
        """
        h_best = None
        inlyer_best = -1
        counter = 0
        for i in range(0,numLoops,4):

            #num loops must be a multiple of 4
            randArr = []
            src, des = [],[]
            for x in range(4):
                run = True
                while run:
                    ii = random.randint(0,len(self.list_of_pairs)-1)
                    if(ii not in randArr):
                        run = False
                        randArr.append(ii)

                #set pairs in each array, src is im1, des is im2 points, determined in outliyer rejection
                src.append(self.list_of_pairs[ii][0]) ## gets first of the pair of II index
                des.append(self.list_of_pairs[ii][1]) ## get second of the pair at II index

            # points aquired
            if(len(src) != 4):
                print("SOMETHING IS WRONG")


            #compute homography of the four points
            h = np.array([])
            h, status = cv2.findHomography(np.array(src), np.array(des))
            # h is a 3 X 3 np array
            #
            num_inlyer = self.compute_h_score(h)
            #print(h,num_inlyer)


            if(num_inlyer > inlyer_best):
                h_best = h
                inlyer_best = num_inlyer
                counter += 1


            if(inlyer_best < 0):
                print("problem with inlyer")
            #compute inliers based on h
            #uses SSD and epsilon as a threshold

        #compute SVD LATER
        #print(inlyer_best, counter)
        return h_best

    def compute_h_score(self, h):
        #compute number of inlyers
        #inlyer is determined if SSD(p' , Hp) < self.epsilon

        inlyer = 0

        for pnt in self.list_of_pairs:
            p = h * pnt[0]
            score = np.linalg.norm(pnt[1] - p)
            #print(score)
            if (score > self.epsilon):
                # inlyer found
                inlyer+=1

        return inlyer

    def SSD(p1, p2):
        #UNSURE
        return p1 - p2

    def dist(self, p1, p2):
        return math.sqrt(p1**2 + p2**2)

    def get_stitch(self):
        pass
