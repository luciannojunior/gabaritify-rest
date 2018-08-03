# USAGE
# python validation.py -d path/to/dataset/

import test_grader
import json_data_reader as reader
import os
import cv2
import argparse
import time

ap = argparse.ArgumentParser()
ap.add_argument("-d", "--dataset", required=True,
	help="path to the input dataset")
args = vars(ap.parse_args())

dataset_dir = args["dataset"] if args["dataset"].endswith("/") else args["dataset"] + "/"
exams = 0
exams_hits = 0
questions = 0
questions_hits = 0
duration = 0.0
s = 4
conf_matrix = [[0 for x in range(s)] for y in range(s)]

for exam_model in os.listdir(dataset_dir):
    for img in os.listdir(dataset_dir + exam_model):
        exams += 1
        image = cv2.imread(dataset_dir + exam_model + "/" + img)
        
        t_start = time.time()
        questionCnts, thresh = test_grader.getFilteredContours(image)
        answers = test_grader.answersFromContours(questionCnts, thresh)[1:]
        t_end = time.time()
        duration += t_end - t_start

        gt_answers = reader.get_student_answers(img)        

        if img.startswith("exam4"): del(answers[3])

        # print "############ " + img
        # print answers
        # print gt_answers
        exam_success = True
        for ans in range(len(answers)):
            questions += 1
            if ans < len(gt_answers):
                conf_matrix[answers[ans]][gt_answers[ans]] += 1
                if answers[ans] == gt_answers[ans]:
                    questions_hits += 1
                else:
                    exam_success = False
            
        if exam_success:
            exams_hits += 1

exams_acc = exams_hits/float(exams)
question_acc = questions_hits/float(questions)
mean_duration = duration/float(exams)

print "ACURACIA DE EXAMES:   " + str(exams_acc)
print "ACURACIA DE QUESTOES: " + str(question_acc)
print "DURACAO MEDIA:        " + str(mean_duration)
print conf_matrix