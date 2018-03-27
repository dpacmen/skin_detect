import numpy as np
import argparse
import cv2

def resize(image, width = None, height = None, inter = cv2.INTER_AREA):
	# initialize the dimensions
	# grab the image size
	dim = None
	(h, w) = image.shape[:2]

	if width is None and height is None:
		return image

	if width is None:
		# calculate the ratio of the height
		ratio = height / float(h)
		dim = (int(w * ratio), height)

	# otherwise, the height is None
	else:
		# calculate the ratio of the width and construct the
		# dimensions
		ratio = width / float(w)
		dim = (width, int(h * ratio))

	# resize the image
	resized_image = cv2.resize(image, dim, interpolation = inter)

	# return the resized image
	return resized_image

#parse arguments from terminal
ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video",type = int)
args = vars(ap.parse_args())

#uppper and lower boundaries of HSV pixel 
#skin intensities
lower = np.array([0, 48, 80], dtype = "uint8")
upper = np.array([20, 255, 255], dtype = "uint8")

#webcam
if not args.get("video", False):
	camera = cv2.VideoCapture(0)
 
#load the video
else:
	camera = cv2.VideoCapture(args["video"])

while True : 

	(grabbed, frame) = camera.read()

	if args.get("video") and not grabbed:
		break

	frame = resize(frame, width = 600)
	hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
	skin_mask = cv2.inRange(hsv_frame, lower, upper)

	#apply erosion and dilation on mask
	structured = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (11,11))
	skin_mask = cv2.erode(skin_mask, structured, iterations = 2)
	skin_mask = cv2.dilate(skin_mask, structured, iterations = 2)

	#blur and apply mask to the frame
	skin_mask = cv2.GaussianBlur(skin_mask, (3,3), 0)
	skin = cv2.bitwise_and(frame, frame, mask = skin_mask)

	cv2.imshow("images", np.hstack([frame, skin]))

	if cv2.waitKey(1) & 0xFF == ord("q"):
		break

camera.release()
cv2.destroyAllWindows()
