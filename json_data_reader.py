import json
import ntpath

json_data = json.load(open("conv.json"))["astruct"]["records"]
test_config = json.load(open("test_config.json"))

def find_exam(image_name):
    for i in range(len(json_data)):
        if json_data[i]["imageName"] == image_name:
            return json_data[i]

# returns a list with the answers for the test of the image received
def get_student_answers(image_name):
    student_answers = []
    student_exam = find_exam(ntpath.basename(image_name))
    q = 0
    for i in range(test_config["numQuestions"]):
        for j in range(test_config["questionsSize"][i]):
            actual_question = student_exam["answerType"][q][0]
            if actual_question == 1:
                student_answers.append(j)
            q += 1
    return student_answers