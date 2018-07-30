from flask import Flask
import test_grader as tester
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/upload', methods=['POST'])
def upload_file():
    file = request.files['image']
    # f = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    answers = tester.analyseImage(file)
    # add your custom code to check that the uploaded file is a valid image and not a malicious file (out-of-scope for this post)
    return answers