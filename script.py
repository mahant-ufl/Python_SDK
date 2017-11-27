from flask import Flask, jsonify, request, redirect, render_template, url_for, send_file
from werkzeug import secure_filename
import requests
app = Flask(__name__)


@app.route('/')
def home_page():
   return 'SDK for initializing and training deep learning models.'


@app.route('/train-and-run-model', methods=['GET', 'POST'])
def train_and_run_model():
    if request.method != 'POST':
        return 'Request method has to be POST'
    else:
        output = redirect(url_for('initialize_model'))
        output = output + ' ' + redirect(url_for('train_model'))
        output = output + ' ' + redirect(url_for('output_results'))
        return output


@app.route('/initialize-model', methods=['GET', 'POST'])
def initialize_model():
    if request.method == 'POST':
        hostname = request.json['hostname']
        port = request.json['port']
        func = request.json['initializing-function']
        return requests.get(hostname + ':' + port + '/' + func).content


@app.route('/train-model', methods=['GET', 'POST'])
def train_model():
    if request.method == 'POST':
        hostname = request.json['hostname']
        port = request.json['port']
        func = request.json['training-function']
        return requests.get(hostname + ':' + port + '/' + func).content


@app.route('/output-results', methods=['GET', 'POST'])
def output_results():
    if request.method == 'POST':
        hostname = request.json['hostname']
        port = request.json['port']
        function = request.json['output-function']
        return requests.get(hostname + ':' + port + '/' + function).content


@app.route('/train-model/args')
def train_model_args():
    if 'hostname' in request.args:
        hostname = request.args['hostname']
        port = request.args['port']
        func = request.args['function']
        return hostname + ':' + port + '/' + func


@app.route('/download')
def download_file():
   return render_template('download.html')


@app.route('/return-file')
def return_file():
   return send_file('static/python.png', attachment_filename='python.png')


@app.route('/upload')
def upload_file():
    return render_template('upload.html')


@app.route('/upload-file', methods=['GET', 'POST'])
def receive_file():
    if request.method == 'POST':
        f = request.files['file']
        f.save(secure_filename(f.filename))
        return 'File uploaded successfully'


@app.route('/post',methods=['GET', 'POST'])
def post_page():
    if request.method == 'POST':
        return 'You are using POST method.'
    else:
        return 'You are using GET method.'


@app.route('/user/login')
def login_page():
   return 'Login Page'


@app.route('/user/<username>')
def show_user_profile(username):
    return 'Hello %s!' % username


@app.route('/guest/<guest>')
def redirect_page(guest):
    if guest == 'admin':
        return redirect(url_for('admin_page'))
    else:
        return redirect(url_for('show_user_profile',username=guest))


language_list = [{'name': 'Javascript'}, {'name': 'Python'}, {'name': 'C++'}]


@app.route('/languages', methods=['GET', 'POST'])
def request_languages():
    if request.method == 'POST':
        language = {'name': request.json['name']}
        language_list.append(language)
        return jsonify({'languages': language_list})
    else:
        return jsonify({'languages': language_list})


@app.route('/languages/<int:language_id>', methods=['GET'])
def request_one(language_id):
    return jsonify({'language' : language_list[language_id]})


@app.route('/post/<int:post_id>')
def show_post(post_id):
    return 'Post %d' % post_id


if __name__ == '__main__':
   app.run(host = '127.0.0.1', port = 4000, debug = True)
