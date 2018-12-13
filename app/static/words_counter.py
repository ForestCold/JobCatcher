import re,collections
import os
import pandas
from nltk.corpus import stopwords

from nltk.stem.lancaster import LancasterStemmer

DEFAULT_JDSET_PATH = os.path.join('.', 'naukri_com-job_sample.csv')
MATCHING_TITLES = ['software', '(?:big data)|(?:machine learning)|(?:data scientist)',
                   '(?:web)|(?:front end)', 'backend', 'full stack',
                   '(?:mobile)|(?:android)|(?:ios)', 'application', 'security', 'network',
                   'Operations', 'business',  'UI ', '(?:database)|(?:SQL)', 'hardware']

def load_jd_dataset(file_path = DEFAULT_JDSET_PATH):
    jds = pandas.read_csv(file_path)
    return jds

def get_title_freq(matching_title = 'software', is_output_to_file = False):
    jds = load_jd_dataset()
    try:
        simple_jds = jds[['jobdescription', 'jobtitle']]
    except:
        print 'no required columns, please check the input data'
        return

    #filter
    simple_jds = simple_jds[simple_jds.jobtitle.str.contains(matching_title, case = False)]

    #count
    freq_list = simple_jds['jobdescription'].apply(lambda x:get_words_freq(x))
    total_title_count = collections.Counter()
    for count in freq_list:
        total_title_count += count

    #clean stopwords and numbers
    stopWords = set(stopwords.words('english'))
    copy = total_title_count.copy()
    for word in copy:
        if word in stopWords or re.match('^[0-9]+$', word) or len(word) == 1:
            del total_title_count[word]

    #store result
    if is_output_to_file:
        output_file = 'output.txt'
        with open(output_file, 'w+') as f:
            for count in total_title_count.most_common():
                f.write(str(count[0]) + ':' + str(count[1]) + '\n')

    return total_title_count.most_common()

def get_words_freq(string, freq_counter = collections.Counter()):
    """count words frequency of a giving string. tolower() and delstem() is applied"""
    try:
        # wordlist = string.split()
        wordlist = re.findall(r"\w+", string.lower())
        st = LancasterStemmer()
        wordlist = [st.stem(word) for word in wordlist]
        freq_counter += collections.Counter(wordlist)
    except:
        pass

    return freq_counter

# def auto_word_counter():
#     for title in MATCHING_TITLES:
#         output_name = str(title.split())


if __name__ == '__main__':
    # jds = load_jd_dataset()
    # get_words_freq(jds['jobdescription'][0])

    # get_words_freq()#
    # print count1
    get_title_freq(matching_title= '(?:database)|(?:SQL)', is_output_to_file= True)
