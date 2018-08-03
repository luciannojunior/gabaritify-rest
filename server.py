from flask import Flask, request
import test_grader as tester
import json
from flask_cors import CORS, cross_origin

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/upload', methods=['POST'])
@cross_origin()
def upload_file():
    file = request.files['imagem']
    # f = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    answers = tester.analyseImage(file)

    # add your custom code to check that the uploaded file is a valid image and not a malicious file (out-of-scope for this post)
    return json.dumps(answers)

if __name__ == '__main__':
    app.run(debug=True)