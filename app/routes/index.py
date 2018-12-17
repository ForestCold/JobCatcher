import json
import os
import sys
import pandas as pd
import string
import pickle

from nltk.corpus import stopwords
from nltk.stem.lancaster import LancasterStemmer
from nltk.tokenize import word_tokenize
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel

from app import app
from flask import Flask, request, flash, redirect, url_for, send_from_directory
from os.path import join
from werkzeug import secure_filename

from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from cStringIO import StringIO
from cv_miner import extract_keywords
from experience_filter import exp_req_filter

debug = True

UPLOAD_FOLDER = 'app/static/uploaded_files'
ALLOWED_EXTENSIONS = set(['pdf'])

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

reload(sys)
sys.setdefaultencoding('utf8')


@app.route('/')
def root():
    global tf, tfidf, df
    # tf, tfidf, df = train()
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

            with open(file_url.replace("pdf", "txt"), 'w') as f:
                f.write(pdf_parser(file_url))

    return json.dumps("uploaded_files/" + filename)


# generate keywords based on a file
@app.route('/analysis/<filename>/', methods=['GET'])
def analysis_file(filename):
    file_url = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    topic_freqs = {'software': load_topic(os.path.join('app/static/', 'topic_software')),
                   'business': load_topic(os.path.join('app/static/', 'topic_business')),
                   'mobile': load_topic(os.path.join('app/static/', 'topic_mobile')),
                   'frontend': load_topic(os.path.join('app/static/', 'topic_frontend')),
                   'security': load_topic(os.path.join('app/static/', 'topic_security')),
                   'network': load_topic(os.path.join('app/static/', 'topic_network')),
                   'operations': load_topic(os.path.join('app/static/', 'topic_operations.txt')),
                   'hardware': load_topic(os.path.join('app/static/', 'topic_hardware.txt')),
                   'backend': load_topic(os.path.join('app/static/', 'topic_backend.txt')),
                   'data': load_topic(os.path.join('app/static/', 'topic_data.txt'))
                   }
    resume_freq = load_resume(file_url.replace("pdf", "txt"))

    cv_info = infer_topic(topic_freqs, resume_freq)
    with open(file_url.replace("pdf", "txt"), 'r') as f:
        resume = f.read()
        print resume
    print extract_keywords(resume)

    cv_info["keywords"] = extract_keywords(resume)

    keyword = json.dumps(cv_info)
    print keyword
    # print keywords(resume,lemmatize=True)
    return keyword;


# recommend jobs based on a file
@app.route('/recommend/<filename>/', methods=['GET'])
def recommend_jobs(filename):
    # global tf, tfidf, df
    with open(os.path.join('app/static/', 'df.pickle'), 'rb') as handle:
        df = pickle.load(handle).fillna('N/A')

    file_url = os.path.join(app.config['UPLOAD_FOLDER'], filename)

    with open(file_url.replace("pdf", "txt"), 'r') as f:
        resume = f.read()
        # recommendation_index = find_jobs_with_conditions(None, None, resume, None, location='Delhi',
        #                                                  experience='1 - 3 yrs')
        recommendation_index = find_jobs(None, None, resume, 10)

    recommendation_job = []
    for index in recommendation_index:
        recommendation_job.append({
            'Company': df['company'][index],
            'Position': df['jobtitle'][index],
            'Url': '#',
            'Location': df['joblocation_address'][index],
            'Description': df['jobdescription'][index],
            'Experience': df['experience'][index]
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
    with open(resume_url.replace("pdf", "txt"), 'r') as f:
        resume = f.read()

    return json.dumps(filter_data, separators=(',', ':'))


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


def train(train_path=os.path.join('app/static/', 'naukri_com-job_sample.csv')):
    stopWords = stopwords.words("english")
    df = pd.read_csv(train_path).fillna('N/A')
    df.dropna(subset=['jobdescription'])
    jd = df['jobdescription'].astype('U').tolist()
    tf = TfidfVectorizer(analyzer='word', stop_words=stopWords)
    tfidf_matrix = tf.fit_transform(jd)
    return tf, tfidf_matrix


def find_jobs(tf, tfidf_matrix, query_content, n):
    with open(os.path.join('app/static/', 'tf.pickle'), 'rb') as handle:
        tf = pickle.load(handle)
    with open(os.path.join('app/static/', 'tfidf.pickle'), 'rb') as handle:
        tfidf = pickle.load(handle)
    with open(os.path.join('app/static/', 'df.pickle'), 'rb') as handle:
        df = pickle.load(handle).fillna('N/A')
        df.dropna(subset=['jobdescription'])
        jd = df['jobdescription'].astype('U').tolist()

    cosine_similarities = linear_kernel(tf.transform([query_content]), tfidf).flatten()
    key_factors = calc_similarity(query_content)
    k_max = max(key_factors)
    k_min = min(key_factors)
    k_range = k_max-k_min
    c_max = max(cosine_similarities)
    c_min = min(cosine_similarities)
    c_range = c_max - c_min
    factor = k_range/c_range*0.8
    tmp_list = [ k_min+(float(x)-k_min)*factor for x in key_factors]
    simlarities = cosine_similarities+tmp_list
    top_n = -1-n
    related_docs_indices = simlarities.argsort()[:top_n:-1]
    print "top {} similar jobs".format(n)
    return related_docs_indices

def find_jobs_with_conditions(tf, tfidf_matrix, query_content, df, year=2, location="Delhi", n=5):
    with open(os.path.join('app/static/', 'tf.pickle'), 'rb') as handle:
        tf = pickle.load(handle)
    with open(os.path.join('app/static/', 'tfidf.pickle'), 'rb') as handle:
        tfidf = pickle.load(handle)
    with open(os.path.join('app/static/', 'df.pickle'), 'rb') as handle:
        df = pickle.load(handle).fillna('N/A')
        df.dropna(subset=['jobdescription'])
    cosine_similarities = linear_kernel(tf.transform([query_content]), tfidf).flatten()
    related_docs_indices = cosine_similarities.argsort()
    selected_df = df.ix[related_docs_indices]
    # selected_df = exp_req_filter(selected_df, low_bound=2)
    experience = str(year)+" -"
    selected_df = selected_df.loc[
        (selected_df['experience'].str.match(experience)) & (selected_df['joblocation_address'].str.match(location))]
    max_len = min(n, len(selected_df))
    return selected_df.index.values.astype(int)[0:max_len]


def purify_sentence(sentence):
    stop = stopwords.words('english') + list(string.punctuation)
    st = LancasterStemmer()
    filtered_sentence = [w for w in word_tokenize(sentence.decode('utf-8').lower()) if
                         w not in stop and not w.isdigit()]
    return filtered_sentence


def load_topic(file_path):
    word_freq = {}
    with open(file_path, 'r') as f:
        data = f.readlines()
        total_count = 0
        for value in data:
            value = value.replace('\n', '')
            key = value.split(':')[0]
            freq = value.split(':')[1]
            total_count += int(freq)
            word_freq[key] = freq
        for key in word_freq:
            word_freq[key] = float(word_freq[key]) / total_count
    return word_freq


def load_resume(file_path):
    with open(file_path, 'r') as f:
        resume = f.read()
    word_list = purify_sentence(resume)
    word_freq = {}
    for word in word_list:
        if word not in word_freq:
            word_freq[word] = 0
        word_freq[word] += 1
    return word_freq


def infer_topic(topics, resume):
    topic_scores = {}
    topic_words = {}
    score = 0
    for topic_word in topics:
        # print topic_word
        for key in resume:
            if key in topics[topic_word]:
                score += topics[topic_word][key] * resume[key]
                if topic_word not in topic_words.keys():
                    topic_words[topic_word] = [key]
                else:
                    topic_words[topic_word].append(key)
        topic_scores[topic_word] = score
        score = 0
    topic_sum = sum(topic_scores.values())
    topic_ratio = {}
    # print "really intersting"
    for val in topic_scores:
        topic_ratio[val] = float(topic_scores[val]) / topic_sum
    res = {}
    for key in topics:
        if key not in topic_words:
            continue
        res[key] = {'percentage': topic_ratio[key], 'words': topic_words[key]}
    return res


def calc_similarity(content):
    with open(os.path.join('app/static/', 'keyword_lists.pickle'), 'rb') as handle:
        keywords_list = pickle.load(handle)
    with open(os.path.join('app/static/', 'df.pickle'), 'rb') as handle:
        df = pickle.load(handle).fillna('N/A')
        df.dropna(subset=['jobdescription'])
        jd = df['jobdescription'].astype('U').tolist()
    resume_keywords = extract_keywords(content)
    same_list=[]
    for lst in keywords_list:
        same_list.append(len(list(set(resume_keywords) & set(lst))))
    return same_list
