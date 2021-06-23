Implement a Harris' corner detector from scratch in python.

Take four pictures of a scene from different angles and positions. The pictures have to have an overlap area between each other. Use your version of Harris' corner detector to stitch these four images and generate a single image.
Crazy video: Use a handheld camera and record 10 seconds of video at 30 frames per second. While recording the video, change the attitude and position of the camera randomly (feel free to be creative...). Use your version of Harris' corner detector in each frame of the video and generate a new video at 10fps showing the corners detected and a counter with the number of corners detected in each frame.
Submit your Harris' Corner detector code, the stitching code including input images and one output image, and the final video showing the detected corners.


Assignment breakdown:

Video marking works well, takes a long time to load though

Image stitching does not work because homographies are not being properly calculated. If you have any notes please let me know! I will still be working on this for my own personal use so any help would be appreciated.

additonally the program can take in just one image and output useful information

How to use examples:

#call image stitching function
./harrisDetector.py --dir=/home/peter/src/harrisDetector/data/imgs/

#call video capture function
./harrisDetector.py --vid=/home/peter/src/harrisDetector/data/crazyVid.mp4

#call single image viewer
./harrisDetector.py --img=/home/peter/src/harrisDetector/data/mr2.jpg

#when using single image viewer
button presses change view of image
0: unchanged
1: smoothed
2: grayscale
3: corners only
4: gaussian x
5: gaussian y
6: unchanged
