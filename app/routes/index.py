import json
import os

from app import app
from flask import Flask, request, flash, redirect, url_for, send_from_directory
from os.path import join
from werkzeug import secure_filename

debug = True

UPLOAD_FOLDER = 'app/static/uploaded_files'
ALLOWED_EXTENSIONS = set(['pdf'])

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def root():
	return app.send_static_file('index.html')

def allowed_file(filename):
	return '.' in filename and \
		filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
	url = ""
	if request.method == 'POST':
		# check if the post request has the file part
		if 'file' not in request.files:
			flash('No file part')
			return redirect(request.url)
		file = request.files['file']
		# if user does not select file, browser also
		# submit an empty part without filename
		if file.filename == '':
			flash('No selected file')
			url = redirect(request.url)
		if file and allowed_file(file.filename):
			filename = secure_filename(file.filename)
			file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
			basedir = os.path.abspath(os.path.dirname(__file__))
			file_dir = os.path.join(basedir.replace("/app/routes",""), app.config['UPLOAD_FOLDER'])
			url = json.dumps("uploaded_files/" + filename)
	return url

# generate keywords based on a file
@app.route('/analysis/<file>/', methods=['GET'])
def analysis_file(file):
	keywords = ["keywordA", "keywordB", "keywordC"];
	return json.dumps(keywords);
