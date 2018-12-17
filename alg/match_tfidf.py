import pandas as pd
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
import pickle
import os

def train(train_path="data.csv"):
    stopWords = stopwords.words("english")
    df = pd.read_csv(train_path)
    jd = df['Job Description'].tolist()

    tf = TfidfVectorizer(analyzer='word', stop_words=stopWords)
    tfidf_matrix = tf.fit_transform(jd)
    return tf, tfidf_matrix



def find_jobs(tf, tfidf_matrix, query_content, n=5 ):
    cosine_similarities = linear_kernel(tf.transform([query_content]), tfidf_matrix).flatten()



    top_n = -1-n
    related_docs_indices = cosine_similarities.argsort()[:top_n:-1]
    print "top {} similar jobs".format(n)
    print related_docs_indices





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
    with open(os.path.join('../app/static/', 'tf.pickle'), 'rb') as handle:
        tf = pickle.load(handle)
    with open(os.path.join('../app/static/', 'tfidf.pickle'), 'rb') as handle:
        tfidf = pickle.load(handle)
    with open(os.path.join('../app/static/', 'df.pickle'), 'rb') as handle:
        df = pickle.load(handle)
    # tf, tfidf, jds = train()
    print find_jobs(tf, tfidf, resume)
