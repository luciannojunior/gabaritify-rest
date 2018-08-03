# USAGE
# python test_grader.py --image images/test_01.png

# import the necessary packages
from imutils.perspective import four_point_transform
from imutils import contours
import numpy as np
import imutils
import cv2
import json_data_reader as reader

def getFilteredContours(image):
	#convert it to grayscale, blur it
	gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
	
	# apply Otsu's thresholding method to binarize the warped
	# piece of paper
	thresh = cv2.threshold(gray, 0, 255,
		cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]

	#Aply mophology
	kernel = np.ones((7,7),np.uint8)
	thresh = cv2.dilate(thresh,kernel,iterations = 1)

	# find contours in the thresholded image, then initialize
	# the list of contours that correspond to questions
	cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
		cv2.CHAIN_APPROX_SIMPLE)
	cnts = cnts[0] if imutils.is_cv2() else cnts[1]
	questionCnts = []

	# image with all contours
	imageAll = image.copy()
	#image with all questions contours
	imageFilter = image.copy()
	# loop over the contours
	for c in cnts:
		# compute the bounding box of the contour, then use the
		# bounding box to derive the aspect ratio
		(x, y, w, h) = cv2.boundingRect(c)
		ar = w / float(h)
		cv2.rectangle(imageAll,(x,y),(x+w,y+h),(0,255,0),2)

		# in order to label the contour as a question, region
		# should be sufficiently wide, sufficiently tall, and
		# have an aspect ratio approximately equal to 1
		area = w * h
		if area > 7000 and ar >= 1.7 and ar <= 2.3:
			questionCnts.append(c)
			cv2.rectangle(imageFilter,(x,y),(x+w,y+h),(0,255,0),2)
	#cv2.imshow("ImagemFilter", imageFilter)
	#cv2.imshow("ImagemAll", imageAll)


	# sort the question contours top-to-bottom, then initialize
	# the total number of correct answers
	questionCnts = contours.sort_contours(questionCnts,
		method="top-to-bottom")[0]

	return (questionCnts, thresh)



def correcAnswerInRow(cnts, thresh):
	bubbled = None
	# loop over the sorted contours
	for (j, c) in enumerate(cnts):
		# construct a mask that reveals only the current
		# "bubble" for the question
		mask = np.zeros(thresh.shape, dtype="uint8")
		cv2.drawContours(mask, [c], -1, 255, -1)
		# apply the mask to the thresholded image, then
		# count the number of non-zero pixels in the
		# bubble area
		mask = cv2.bitwise_and(thresh, thresh, mask=mask)
		total = cv2.countNonZero(mask)

		# if the current total has a larger number of total
		# non-zero pixels, then we are examining the currently
		# bubbled-in answer
		#print(total, j)
		if bubbled is None or total > bubbled[0]:
			bubbled = (total, j)
	return bubbled

def answersFromContours(questionCnts, thresh):
	answers = []
	for (q, i) in enumerate(np.arange(0, len(questionCnts), 4)):
		# sort the contours for the current question from
		# left to right, then initialize the index of the
		# bubbled answer
		cnts = contours.sort_contours(questionCnts[i:i + 4])[0]
		bubbled = correcAnswerInRow(cnts, thresh)
		# check to see if the bubbled answer is correct
		answers.append(bubbled[1])
	return answers

# Gets an image and returns its answers wrote in paper as an array
def analyseImage(image):
	# readImage = cv2.imdecode(np.asarray(image), cv2.IMREAD_COLOR)
	readImage = cv2.imdecode(np.fromstring(image.read(), np.uint8), cv2.IMREAD_COLOR)
	questionCnts, thresh = getFilteredContours(readImage)
	print 'CHEGOU NO QUESTION'
	answers = answersFromContours(questionCnts, thresh)
	print answers


	return answers