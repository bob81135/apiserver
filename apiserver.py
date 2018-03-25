import os
from flask import Flask, render_template, request, redirect, url_for, send_from_directory
from werkzeug import secure_filename
import json
from flask import Flask, request
from flask_cors import CORS,cross_origin
from flask_restful import Resource, Api
import urllib.request

app = Flask(__name__)
CORS(app)
app.config['UPLOAD_FOLDER'] = app.root_path+'/img'
app.config['ALLOWED_EXTENSIONS'] = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

#check
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']

#upload
@app.route('/upload', methods=['POST'])
def upload():
    filenames = []

    tag = request.form.get('tag')
    Id = request.form.get('id')
    uploaded_files = request.files.getlist("file[]")

    imgpath = app.config['UPLOAD_FOLDER'] +'/'+Id
    if not os.path.isdir(imgpath):
        os.mkdir(imgpath)
    if not os.path.isdir(imgpath+'/'+tag):
        os.mkdir(imgpath+'/'+tag)
    for file in uploaded_files:
        if file and allowed_file(file.filename):   
            filename = secure_filename(file.filename) 
            file.save(os.path.join(imgpath+'/'+tag, filename))   
            filenames.append(filename)  
    
    return "success"

@app.route('/train', methods=['POST'])
def train():
    name = request.form.get('name')
    os.system("python3 ~/tensorflow/tensorflow/examples/image_retraining/retrain.py --image_dir ~/flask/img/"+name)   
    return "success"
#download
@app.route('/file', methods=['GET'])
def givefile(): 
    uploads = os.path.join("/home/test/flask/pb/")
    return send_from_directory(uploads, "output_graph.pb", as_attachment = True)

@app.route('/file1', methods=['GET'])
def givefile1(): 
    uploads = os.path.join("/home/test/flask/pb/")
    return send_from_directory(uploads, "output_labels.txt", as_attachment = True)
#main
if __name__ == '__main__':
    app.run('10.26.1.225', 5000, debug = True)


