import json
import os

from app import app
from flask import Flask, request
from werkzeug import secure_filename

debug = False

UPLOAD_FOLDER = 'app/data'

@app.route('/')
def root():
	return app.send_static_file('index.html')

@app.route('/list')
def _list():
	datalist = [name for name in os.listdir("app/data")]

	if ".DS_Store" in datalist:
		datalist.remove(".DS_Store")

	return json.dumps(datalist)

#load raw data
@app.route('/data')
def _load():

	data = {}

	# add data loader here

	return json.dumps(data)
