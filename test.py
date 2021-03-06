import os
from flask import Flask, render_template, request, redirect, url_for, send_from_directory
from werkzeug import secure_filename
import json
#rom flask import Flask, request
from flask_cors import CORS, cross_origin
#from flask_restful import Resource, Api
import urllib.request
from PIL import Image
import mimetypes

app = Flask(__name__)
CORS(app)
app.config['UPLOAD_FOLDER'] = app.root_path+'/img'
app.config['ALLOWED_EXTENSIONS'] = set(
    ['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

# check

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']

# upload

@app.route('/upload', methods=['POST'])
def upload():
    filenames = []

    tag = request.form.get('tag')
    Id = request.form.get('id')
    uploaded_files = request.files.getlist("file[]")
    if not tag or not Id:
        return "1"
    imgpath = app.config['UPLOAD_FOLDER'] + '/'+Id
    if not os.path.isdir(imgpath):
        os.mkdir(imgpath)
    if not os.path.isdir(imgpath+'/'+tag):
        os.mkdir(imgpath+'/'+tag)
    for file in uploaded_files:
        file_mime = mimetypes.guess_type(file.filename)
        print(file_mime[0])
        if file_mime[0] != "image/jpeg":
            return "1"
        filename = secure_filename(file.filename)
        file.save(os.path.join(imgpath+'/'+tag, filename))
        im = Image.open(os.path.join(imgpath+'/'+tag, filename))
        width = 233
        ratio = float(width)/im.size[0]
        height = int(im.size[1]*ratio)
        nim = im.resize((width, height), Image.BILINEAR)
        nim.save(os.path.join(imgpath+'/'+tag, filename))
        filenames.append(filename)
        #print (os.path.isfile(imgpath+'/'+tag+'/'+filename))
    return "0"


@app.route('/train', methods=['POST'])
def train():
    name = request.form.get('name')
    if not name:
        return "1"
    top = app.config['UPLOAD_FOLDER']+"/" +name
    if not os.path.isdir(top):
        return "1"
    for dirPath, dirNames, fileNames in os.walk(top):
        #print(len(dirNames))
        #print(len(fileNames))
        if dirPath == top:
            if len(dirNames) < 2:
                return "1"
        else:
            if len(fileNames) < 20:
                return "1"
    os.system("python3 ~/flask/tensorflow/tensorflow/examples/image_retraining/retrain.py --image_dir ~/flask/img/"+name)
    os.system("python3 /home/an/flask/tensorflow/tensorflow/python/tools/optimize_for_inference.py --input=/home/an/flask/pb/output_graph.pb --output=/home/an/flask/pb/test.pb --input_names=Mul --output_names=final_result")
    if  os.path.exists("version.txt"):
        with open("version.txt", 'r') as f:
            a = f.read()
            print(str(a))
        with open("version.txt", 'w') as f:
            b = int(a)+1
            f.write(str(b))
    else:
        with open("version.txt", 'w') as f:
            f.write('1')
    return "0"
        
@app.route('/file', methods=['GET'])
def givefile():
    uploads = os.path.join("/home/an/flask/pb/")
    return send_from_directory(uploads, "test.pb", as_attachment=True)


@app.route('/file1', methods=['GET'])
def givefile1():
    uploads = os.path.join("/home/an/flask/pb/")
    return send_from_directory(uploads, "output_labels.txt", as_attachment=True)


# main
if __name__ == '__main__':
    app.run('127.0.0.1', 5000, debug=True)
