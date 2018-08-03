import argparse
import cv2
import test_grader as tester

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True,
	help="path to the input image")
args = vars(ap.parse_args())

# load the image, 
# slightly, then find edges
image = cv2.imread(args["image"])
questionCnts, thresh = tester.getFilteredContours(image)
answers = tester.answersFromContours(questionCnts, thresh)
print("ANSWERS DETECTED: " + str(answers))
