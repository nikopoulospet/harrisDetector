import numpy as np

class Detector:
    def __init__(self,W,H,sigma,alpha):
        """
        Harris detector class
        preforms harris detection on a given image
        """
        #system control params
        self.reset = False

        #global constants
        self.W = W
        self.H = H
        self.sigma = sigma
        self.alpha = alpha

        #Thresholding params
        self.rThresh = 500000
        self.rMax = 0

        #gaussian / filter parameters
        self.gSize = 3
        self.gaussianWeights = self.compute_gaussian_weights()
        self.dyOperator = np.array([[1,2,1],[0,0,0],[-1,-2,-1]])
        self.dxOperator = np.array([[1,0,-1],[2,0,-2],[1,0,-1]])

        #private image maps, hold computed information on an image
        self.__lamdaF = np.array([])
        self.__image = np.array([])
        self.__rMap = np.array([])
        self.__original = None

    def set_image(self, img):
        self.__original = img
        self.__image = np.pad(img, (self.gSize//2,self.gSize//2), 'edge')
        self.__lamdaF = np.full((self.__image[:,0].size,self.__image[0,:].size,2),1)
        self.__rMap = np.full((self.__image[:,0].size,self.__image[0,:].size),0) ## use RMAP as feature descriptors

    def get_image(self):
        return self.__image[self.gSize//2:self.H+self.gSize//2,self.gSize//2:self.W+self.gSize//2]

    def get_lamdaF(self):
        return self.__lamdaF[self.gSize//2:self.H+self.gSize//2,self.gSize//2:self.W+self.gSize//2]

    def get_rMap(self):
        return self.__rMap[self.gSize//2:self.H+self.gSize//2,self.gSize//2:self.W+self.gSize//2]

    def get_points(self):
        arr = []
        for x in range(0,self.__image[0,:].size):
            for y in range(0,self.__image[:,0].size):
                if self.__rMap[y][x] != 0:
                    arr.append((x,y))

        return arr

    def reset_detector_arrays(self):
        self.reset = False
        self.set_image(self.__original)

    def find_interest_points(self):
        if(self.__image.size == 0):
            return False

        #find gaussians
        self.compute_gaussian_maps()

        #solve for M and compute function R
        self.compute_moment_and_R()

        #threshold R
        self.threshold_R()

        #non maximum supression
        self.window_based_nms()

        return True

    def derivative_arr(self, x, y):
        return np.array([[self.__lamdaF[y][x][0]**2, self.__lamdaF[y][x][0]*self.__lamdaF[y][x][1]],
                      [self.__lamdaF[y][x][0]*self.__lamdaF[y][x][1], self.__lamdaF[y][x][1]**2]])

    def compute_moment_and_R(self):
        #for all elements in the image compute a 2X2 matrix M and solve for R
        #window size is based on gaussian window defined in __init__

        self.rMax = 0;
        for x in range(0,self.__image[0,:].size):
            for y in range(0,self.__image[:,0].size):
                #if index is outside of image and padding
                xmin,xmax = x-self.gSize//2, x+self.gSize//2
                ymin,ymax = y-self.gSize//2, y+self.gSize//2
                if(xmin < 0 or ymin< 0 or xmax >= self.__image[0,:].size or ymax >= self.__image[:,0].size):
                    continue

                #compute M
                M = np.array([[0.,0.],[0.,0.]])
                offset = self.gSize//2
                for i in range(-offset,offset+1):
                    for ii in range(-offset,offset+1):

                        temp = self.derivative_arr(i+x,i+y)
                        M += self.gaussianWeights[i+offset][ii+offset] * temp

                #compute R
                self.__rMap[y][x] = np.linalg.det(M) - self.alpha * (np.trace(M)**2)
                self.rMax = max(self.rMax,self.__rMap[y][x])

    def threshold_R(self):
        for x in range(0,self.__image[0,:].size):
            for y in range(0,self.__image[:,0].size):
                if(self.__rMap[y][x] < self.rThresh):
                    self.__rMap[y][x] = 0

    def smooth_img(self):
        if(self.__image.size == 0):
            return False

        for x in range(0,self.__image[0,:].size):
            for y in range(0,self.__image[:,0].size):
                #if index is outside of image and padding
                xmin,xmax = x-self.gSize//2, x+self.gSize//2
                ymin,ymax = y-self.gSize//2, y+self.gSize//2
                if(xmin < 0 or ymin< 0 or xmax >= self.__image[0,:].size or ymax >= self.__image[:,0].size):
                    continue
                self.__image[y][x] =  np.sum(self.gaussianWeights * self.__image[ymin:ymax+1,xmin:xmax+1])
        return True

    def compute_gaussian_maps(self):
        for x in range(0,self.__image[0,:].size):
            for y in range(0,self.__image[:,0].size):
                #if index is outside of image and padding
                xmin,xmax = x-1, x+1
                ymin,ymax = y-1, y+1
                if(xmin < 0 or ymin< 0 or xmax >= self.__image[0,:].size or ymax >= self.__image[:,0].size):
                    continue
                self.__lamdaF[y][x][0] =  np.sum(self.dxOperator * self.__image[ymin:ymax+1,xmin:xmax+1])
                self.__lamdaF[y][x][1] =  np.sum(self.dyOperator * self.__image[ymin:ymax+1,xmin:xmax+1])

    def window_based_nms(self):
        if(self.__image.size == 0):
            return False

        for x in range(0,self.__image[0,:].size):
            for y in range(0,self.__image[:,0].size):
                #if index is outside of image and padding
                xmin,xmax = x-3, x+3
                ymin,ymax = y-3, y+3
                if(xmin < 0 or ymin< 0 or xmax >= self.__image[0,:].size or ymax >= self.__image[:,0].size):
                    continue
                if(self.__rMap[y][x] < np.max(self.__rMap[ymin:ymax+1,xmin:xmax+1])):
                    self.__rMap[y][x] = 0

        return True

    def compute_gaussian_weights(self):
        """
        creates gaussian kernel with side length and a sigma
        """

        ax = np.linspace(-(self.gSize - 1) / 2., (self.gSize - 1) / 2., self.gSize)
        xx, yy = np.meshgrid(ax, ax)

        kernel = np.exp(-0.5 * (np.square(xx) + np.square(yy)) / np.square(self.sigma))
        return kernel / np.sum(kernel)

