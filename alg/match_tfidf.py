import pandas as pd
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel

def train(train_path="data.csv"):
    stopWords = stopwords.words("english")
    df = pd.read_csv(train_path)
    jd = df['Job Description'].tolist()

    tf = TfidfVectorizer(analyzer='word', stop_words=stopWords)
    tfidf_matrix = tf.fit_transform(jd)
    return tf, tfidf_matrix

def find_jobs(tf, tfidf_matrix, query_content):
    cosine_similarities = linear_kernel(tf.transform([query_content]), tfidf_matrix).flatten()
    related_docs_indices = cosine_similarities.argsort()[:-6:-1]
    print "top 5 similar jobs"
    print related_docs_indices

if __name__ == "__main__":
    with open('resume_extracted.txt', 'r') as f:
        resume = f.read()
    tf, tfidf = train()
    find_jobs(tf, tfidf, resume)
