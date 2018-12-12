import json
import os
import sys
import pandas as pd

from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
from gensim.summarization import keywords

from app import app
from flask import Flask, request, flash, redirect, url_for, send_from_directory
from os.path import join
from werkzeug import secure_filename

from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from cStringIO import StringIO

debug = True

UPLOAD_FOLDER = 'app/static/uploaded_files'
ALLOWED_EXTENSIONS = set(['pdf'])

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

reload(sys)
sys.setdefaultencoding('utf8')

@app.route('/')
def root():
	global tf, tfidf
	tf, tfidf = train()
	return app.send_static_file('index.html')

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
			file_url = os.path.join(app.config['UPLOAD_FOLDER'], filename)
			file.save(file_url)

			with open(file_url.replace("pdf","txt"), 'w') as f:
			    f.write(pdf_parser(file_url))

	return json.dumps("uploaded_files/" + filename)

# generate keywords based on a file
@app.route('/analysis/<filename>/', methods=['GET'])
def analysis_file(filename):
	file_url = os.path.join(app.config['UPLOAD_FOLDER'], filename)
	with open(file_url.replace("pdf","txt"), 'r') as f:
		resume = f.read()

	print keywords(resume,lemmatize=True)
	keyword = ["keywordA", "keywordB", "keywordC"];
	return json.dumps(keyword);

# recommend jobs based on a file
@app.route('/recommend/<filename>/', methods=['GET'])
def recommend_jobs(filename):

	global tf, tfidf, df
	file_url = os.path.join(app.config['UPLOAD_FOLDER'], filename)

	with open(file_url.replace("pdf","txt"), 'r') as f:
		resume = f.read()
		recommendation_index = find_jobs(tf, tfidf, resume)

	recommendation_job = []
	for index in recommendation_index:
		recommendation_job.append({
			'Company' : df['company'][index],
			'Position' : df['jobtitle'][index],
			'Url' : '#',
			'Location' : df['joblocation_address'][index],
			'Description' : df['jobdescription'][index],
			'Experience' : df['experience'][index]
		})

	return json.dumps(recommendation_job)

# update recommend jobs based on a file
@app.route('/update_recommendation/<filter_data>/', methods=['GET'])
def update_recommend_jobs(filter_data):
	data = json.loads(filter_data)
	number = data["number"]
	location = data["location"]
	experience = data["experience"]
	resume_url = os.path.join(app.config['UPLOAD_FOLDER'], data["resume"])
	with open(resume_url.replace("pdf","txt"), 'r') as f:
		resume = f.read()

	# recommend jobs

	return json.dumps(filter_data, separators=(',',':'))

# private util functions #
def allowed_file(filename):
	return '.' in filename and \
		filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def pdf_parser(pdf):
	fp = file(pdf, 'r')
	rsrcmgr = PDFResourceManager()
	retstr = StringIO()
	laparams = LAParams()
	device = TextConverter(rsrcmgr, retstr, codec='utf-8', laparams=laparams)
	interpreter = PDFPageInterpreter(rsrcmgr, device)

	for page in PDFPage.get_pages(fp):
		interpreter.process_page(page)
		data = retstr.getvalue()

		return data

def train(train_path = os.path.join('app/static/', 'naukri_com-job_sample.csv')):
	global df
	stopWords = stopwords.words("english")
	df = pd.read_csv(train_path).fillna('N/A')

	df.dropna(subset=['jobdescription'])
	jd = df['jobdescription'].astype('U').tolist()

	tf = TfidfVectorizer(analyzer='word', stop_words=stopWords)
	tfidf_matrix = tf.fit_transform(jd)
	return tf, tfidf_matrix

def find_jobs(tf, tfidf_matrix, query_content):
	cosine_similarities = linear_kernel(tf.transform([query_content]), tfidf_matrix).flatten()
	related_docs_indices = cosine_similarities.argsort()[:-11:-1]
	return related_docs_indices
