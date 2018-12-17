import os
import pickle
import sys
import numpy as np

from cv_miner import extract_keywords

reload(sys)
sys.setdefaultencoding('utf8')


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
    topic_sum = sum(topic_scores.values())
    topic_ratio = {}
    for val in topic_scores:
        topic_ratio[val]=float(topic_scores[val])/topic_sum
    res = {}
    for key in topics:
        res[key]={'percentage':topic_ratio[key], 'words':topic_words[key]}
    return res


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
    print np.argsort(same_list)
    result_list = np.argsort(same_list)[::-1][:10]
    for x in result_list:
        print jd[x]
    print same_list

if __name__ == "__main__":
    # with open(os.path.join('./', 'df.pickle'), 'rb') as handle:
    #     df = pickle.load(handle)
    #     df.dropna(subset=['jobdescription'])
    #     jd = df['jobdescription'].astype('U').tolist()
    # keyword_list = []
    # for i in range(len(jd)):
    #     keyword_list.append(extract_keywords(jd[i]))
    #     if i%100==0:
    #         print i
    # with open('keyword_lists.pickle', 'wb') as handle:
    #     pickle.dump(keyword_list, handle, protocol=pickle.HIGHEST_PROTOCOL)

    # with open(os.path.join('./', 'keyword_lists.pickle'), 'rb') as handle:
    #     keywords_list = pickle.load(handle)
    # print keywords_list
    with open('./uploaded_files/Resume_Yami.txt') as f:
        content = f.read()
        calc_similarity(content)