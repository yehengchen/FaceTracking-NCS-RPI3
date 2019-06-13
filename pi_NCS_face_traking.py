import cv2
import time
import numpy
from multiprocessing import Process
from multiprocessing import Queue
from functools import partial
from picamera.array import PiRGBArray
from picamera import PiCamera
import multiprocessing as mp
import os

# Load the face detection model
net = cv2.dnn.readNet('models/face-detection-retail-0004.xml', 'models/face-detection-retail-0004.bin')

'''
# Load the age age-gender-recognition model
model_path = "models/age-gender-recognition-retail-0013.xml"
pbtxt_path = "models/age-gender-recognition-retail-0013.bin"
net1 = cv2.dnn.readNet(model_path, pbtxt_path)
#face_cascade = cv2.CascadeClassifier('models/haarcascade_frontalface_default.xml')
net1.setPreferableTarget(cv2.dnn.DNN_TARGET_MYRIAD)
'''

# Specify target device
net.setPreferableTarget(cv2.dnn.DNN_TARGET_MYRIAD)

# Misc vars
font = cv2.FONT_HERSHEY_SIMPLEX

frameWidth = 320
frameHeight = 240
"""
frameWidth = 640
frameHeight = 480
secPerFrame = 0.0
"""
### Setup #####################################################################
 
os.putenv( 'SDL_FBDEV', '/dev/fb0' )
 
resX = 320
resY = 240
 
cx = resX / 2
cy = resY / 2

# Servo_init
os.system( "echo 0=130 > /dev/servoblaster" )
os.system( "echo 1=170 > /dev/servoblaster" )
 
xdeg = 130
ydeg = 170

# Test Video path
#videopath = ("/home/pi/workspace/RPi3_NCS2/home/pi/workspace/RPi3_NCS2/car_test_video.avi")

# Picam
camera = PiCamera()
camera.rotation = 180
camera.resolution = (320,240)
camera.framerate = 35
rawCapture = PiRGBArray(camera, size=(320,240)) 

# Allow the camera to warmup
time.sleep(0.1)

"""
# USBcam
cap = cv2.VideoCapture(0)

#Get the camera data:
def capProperties():
	print("[info] W, H, FPS")
	print(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
	print(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
	print(cap.get(cv2.CAP_PROP_FPS))

capProperties()
cap.set(cv2.CAP_PROP_FRAME_WIDTH, frameWidth)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, frameHeight)
"""

#time the frame rate....
start = time.time()
frames = 0

def classify_frame(net, inputQueue, outputQueue):
# keep looping
	while True:
		# check to see if there is a frame in our input queue
		if not inputQueue.empty():
			# grab the frame from the input queue, resize it, and
			# construct a blob from it
			frame = inputQueue.get()
			frame = cv2.resize(frame, (300, 300))

			blob = cv2.dnn.blobFromImage(frame, size=(300, 300), ddepth=cv2.CV_8U) 

			net.setInput(blob)
			out = net.forward()
			# write the detections to the output queue
			outputQueue.put(out)

# initialize the input queue (frames), output queue (out),
# and the list of actual detections returned by the child process
inputQueue = Queue(maxsize=1)
outputQueue = Queue(maxsize=1)
out = None

# construct a child process *indepedent* from our main process of
# execution
print("[INFO] starting process...")
p = Process(target=classify_frame, args=(net,inputQueue,outputQueue,))
p.daemon = True
p.start()

print("[INFO] starting capture...")
face_count = 0

for frame in camera.capture_continuous(rawCapture, format="rgb", use_video_port=True):
#while(True):#USBcam
	# Capture frame-by-frame
	#ret, frame = cap.read()
	
	#Picam
	frame = frame.array
	# if the input queue *is* empty, give the current frame to
	# classify
	if inputQueue.empty():
		inputQueue.put(frame)

	# if the output queue *is not* empty, grab the detections
	if not outputQueue.empty():
		out = outputQueue.get()


	# check to see if 'out' is not empty
	if out is not None:
	# loop over the detections
		# Draw detections on the frame
		for detection in out.reshape(-1, 7):

			confidence = float(detection[2])

			xmin = int(detection[3] * frame.shape[1])
			ymin = int(detection[4] * frame.shape[0])
			xmax = int(detection[5] * frame.shape[1])
			ymax = int(detection[6] * frame.shape[0])

			if confidence > 0.5:
				face_count += 1
				print(face_count)
				#bounding box
				cv2.rectangle(frame, (xmin, ymin), (xmax, ymax), color=(0, 255, 255))

				#label
				cv2.rectangle(frame, (xmin-1, ymin-1),\
				(xmin+60, ymin-10), (0,255,255), -1)
				#labeltext
				cv2.putText(frame,'Face'+ str(face_count) +':' + str(round(confidence,2)),\
				(xmin,ymin-2), font, 0.3,(0,0,0),1,cv2.LINE_AA)
				
				#ServoBlaster
				tx = (xmin + xmax)/2
				ty = (ymin + ymax)/2
				
				if   ( cx - tx > 15 and xdeg <= 180 ): 
					xdeg += 0.5
					os.system( "echo 0=" + str( xdeg ) + " > /dev/servoblaster" )
				elif ( cx - tx < -15 and xdeg >= 90 ):
					xdeg -= 0.5
					os.system( "echo 0=" + str( xdeg ) + " > /dev/servoblaster" )
				
				
				if   ( cy - ty > 15 and ydeg >= 90 ):
					ydeg -= 2
					os.system( "echo 1=" + str( ydeg ) + " > /dev/servoblaster" )
				elif ( cy - ty < -15 and ydeg <= 180 ): 
					ydeg += 2 
					os.system( "echo 1=" + str( ydeg ) + " > /dev/servoblaster" )
				'''
				#age
				if((xmax-xmin)>0 and (ymax-ymin)>0):
					facearea = frame[ymin:ymax, xmin:xmax]
					#print(facearea)

					blob = cv2.dnn.blobFromImage(facearea, size=(62, 62), ddepth=cv2.CV_8U)

					net1.setInput(blob)

					out1 = net1.forward()

					num_age = out1[0][0][0][0]

					num_sex = out1[0][1][0][0]

					age = int(num_age*100)

					if(num_sex>0.5):

						sex = "man"

					else:

						sex = "woman"

						txt = "sex: {}, age: {}".format(sex,age)

					if(age<=1):

						txt = "sex: {}, age: {}".format(sex,'?')

					if(i % 2 == 0):

						cv2.putText(frame,txt,(int(xmin), int(ymin)),cv2.FONT_HERSHEY_SIMPLEX,0.65,(255, 255, 0), 2)

					else:

						cv2.putText(frame,txt,(int(xmin), int(ymax)),cv2.FONT_HERSHEY_SIMPLEX,0.65,(255, 255, 0), 2)
				'''
	# Display the resulting frame
	cv2.namedWindow('frame',cv2.WINDOW_NORMAL)
	cv2.resizeWindow('frame',frameWidth,frameHeight)
	newframe = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
	cv2.imshow('frame',newframe)
	rawCapture.truncate(0)

	frames+=1


	if cv2.waitKey(1) & 0xFF == ord('q'):
        	break


end = time.time()
seconds = end-start
fps = frames/seconds
print("Avg Frames Per Sec: "+str(fps))

# When everything done, release the capture
#cap.release()
cv2.destroyAllWindows()


