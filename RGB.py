import picamera
import picamera.array
import time
import numpy as np
import cv2
import io
import datetime
from time import sleep
from datetime import datetime, timedelta

def PreviewOpencvJpeg(camera):
    with io.BytesIO() as stream:
        for frame in camera.capture_continuous(stream, format='jpeg', splitter_port = 2, resize = (320,240), use_video_port=True):
            data = np.fromstring(frame.getvalue(),dtype=np.unit8)
            d1 = datetime.datetime.now()
            cv_image = cv2.imdecode(data,1)
            d = datetime.datetime.now() - d1
            print ("consuming %dms" % (d.microseconds/1000))
            print (cv_image.shape)
            cv2.imwrite("{timestamp:%Y-%m-%d-%H-%M-%S}.png", cv_image)
            stream.seek(0)
            stream.trncate(0)
            

with picamera.PiCamera() as camera:
    camera.preview_fullscreen = False
    camera.preview_window = (5,-20,600,500)
    #camera.resolution = (1024,768)
    camera.resolution = (1920,1680)
    camera.framerate = (25)
    camera.start_preview()
    camera.annotate_text = "experiment"
    camera.vflip = True
    camera.hflip = True
    time.sleep(1)
    for filename in camera.capture_continuous('image{timestamp:%Y-%m-%d-%H-%M-%S}.jpeg'):
        print('Captured %s' % filename)
        time.sleep(120)
    print ("start preview direct from GPU")
#     camera.start_preview()
    PreviewOpencvJpeg(camera)
    
