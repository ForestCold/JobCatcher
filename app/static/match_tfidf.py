import pandas as pd
import pickle
import os
import numpy as np
import sys

from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
from cv_miner import extract_keywords

reload(sys)
sys.setdefaultencoding('utf8')


def train(train_path="data.csv"):
    stopWords = stopwords.words("english")
    df = pd.read_csv(train_path)
    jd = df['Job Description'].tolist()

    tf = TfidfVectorizer(analyzer='word', stop_words=stopWords)
    tfidf_matrix = tf.fit_transform(jd)
    return tf, tfidf_matrix




def find_jobs(tf, tfidf_matrix, query_content, n=5 ):
    with open(os.path.join('./', 'df.pickle'), 'rb') as handle:
        df = pickle.load(handle)
        df.dropna(subset=['jobdescription'])
        jd = df['jobdescription'].astype('U').tolist()

    cosine_similarities = linear_kernel(tf.transform([query_content]), tfidf_matrix).flatten()
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
    # print related_docs_indices


def calc_similarity(content):
    with open(os.path.join('./', 'keyword_lists.pickle'), 'rb') as handle:
        keywords_list = pickle.load(handle)
    with open(os.path.join('./', 'df.pickle'), 'rb') as handle:
        df = pickle.load(handle)
        df.dropna(subset=['jobdescription'])
        jd = df['jobdescription'].astype('U').tolist()
    resume_keywords = extract_keywords(content)
    same_list=[]
    for lst in keywords_list:
        same_list.append(len(list(set(resume_keywords) & set(lst))))
    return same_list


if __name__ == "__main__":
    with open('resume_extracted2.txt', 'r') as f:
        resume = f.read()
    # tf, tfidf, jds, df = train("naukri.csv")
    # with open('tf.pickle', 'wb') as handle:
    #     pickle.dump(tf, handle, protocol=pickle.HIGHEST_PROTOCOL)
    #
    # with open('tfidf.pickle', 'wb') as handle:
    #     pickle.dump(tfidf, handle, protocol=pickle.HIGHEST_PROTOCOL)
    #
    # with open('df.pickle', 'wb') as handle:
    #     pickle.dump(df, handle, protocol=pickle.HIGHEST_PROTOCOL)
    with open(os.path.join('.', 'tf.pickle'), 'rb') as handle:
        tf = pickle.load(handle)
    with open(os.path.join('.', 'tfidf.pickle'), 'rb') as handle:
        tfidf = pickle.load(handle)
    with open(os.path.join('.', 'df.pickle'), 'rb') as handle:
        df = pickle.load(handle)
    # tf, tfidf, jds = train()
    print find_jobs(tf, tfidf, resume)
