# USAGE
# python validation.py -d path/to/dataset/

import test_grader
import json_data_reader as reader
import os
import cv2
import argparse

ap = argparse.ArgumentParser()
ap.add_argument("-d", "--dataset", required=True,
	help="path to the input dataset")
args = vars(ap.parse_args())

dataset_dir = args["dataset"] if args["dataset"].endswith("/") else args["dataset"] + "/"
exams = 0
exams_hits = 0
questions = 0
questions_hits = 0

for exam_model in os.listdir(dataset_dir):
    for img in os.listdir(dataset_dir + exam_model):
        exams += 1
        image = cv2.imread(dataset_dir + exam_model + "/" + img)
        questionCnts, thresh = test_grader.getFilteredContours(image)
        answers = test_grader.answersFromContours(questionCnts, thresh)[1:]
        gt_answers = reader.get_student_answers(img)
        # print answers
        # print gt_answers
        # print "############ " + img
        for ans in range(len(answers)):
            questions += 1
            exam_success = True
            if ans < len(gt_answers) and answers[ans] == gt_answers[ans]:
                questions_hits += 1
            else:
                exam_success = False
        if exam_success:
            exams_hits += 1

exams_acc = exams_hits/float(exams)
question_acc = questions_hits/float(questions)
print exams_acc
print question_acc