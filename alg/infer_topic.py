from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem.lancaster import LancasterStemmer
import sys
import json
import string

reload(sys)
sys.setdefaultencoding('utf8')


def purify_sentence(sentence):
    stop = stopwords.words('english') + list(string.punctuation)
    st = LancasterStemmer()
    filtered_sentence = [st.stem(w) for w in word_tokenize(sentence.decode('utf-8').lower()) if
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
    # print word_freq
    return word_freq
    # print sum(word_freq.values())


def load_resume(file_path):
    with open(file_path, 'r') as f:
        resume = f.read()
    word_list = purify_sentence(resume)
    word_freq = {}
    for word in word_list:
        if word not in word_freq:
            word_freq[word] = 0
        word_freq[word] += 1
    # print word_freq
    return word_freq


def infer_topic(topics, resume):
    topic_scores = {}
    topic_words = {}
    score = 0
    for topic_word in topics:
        for key in resume:
            if key in topics[topic_word]:
                score += topics[topic_word][key] * resume[key]
                if topic_word not in topic_words.keys():
                    topic_words[topic_word] = [key]
                else:
                    topic_words[topic_word].append(key)
        topic_scores[topic_word] = score
        score = 0
    # print topic_words
    topic_sum = sum(topic_scores.values())
    topic_ratio = {}
    for val in topic_scores:
        topic_ratio[val]=float(topic_scores[val])/topic_sum
    # print topic_ratio
    res = {}
    for key in topics:
        res[key]={'percentage':topic_ratio[key], 'words':topic_words[key]}
    # dic = {'software': {'percentage': 0.4, 'words': ['soft', 'develop']}}
    print res
    return topic_scores, topic_words


if __name__ == "__main__":
    topic_freqs = {'software':load_topic('topic_software'),
                   'data':load_topic('topic_data'),
                   'business':load_topic('topic_business'),
                   'mobile':load_topic('topic_mobile'),
                   'web':load_topic('topic_web'),
                   }
    resume_freq = load_resume('resume_extracted2.txt')
    infer_topic(topic_freqs, resume_freq)
