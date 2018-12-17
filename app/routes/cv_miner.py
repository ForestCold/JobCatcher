import yaml
import re
import os

CONF_PATH = os.path.join('app/static/confs', 'config.yaml')
CONFS = None

EMAIL_REGEX = r"[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,4}"
PHONE_REGEX = r"\(?(\d{3})?\)?[\s\.-]{0,2}?(\d{3})[\s\.-]{0,2}(\d{4})"


# TODO: phone number and email extract

def load_confs(confs_path=CONF_PATH):
    global CONFS

    if CONFS is None:
        try:
            CONFS = yaml.load(open(confs_path))
        except IOError:
            confs_template_path = confs_path + '.template'
            CONFS = yaml.load(open(confs_template_path))
    return CONFS


def get_conf(conf_name):
    return load_confs()[conf_name]


def extract_fields(cv_string):
    extract_result = []
    for skill_field, list_of_skill in get_conf('extractors').items():
        extract_result += extract_skills(cv_string, skill_field, list_of_skill)
    return extract_result


def extract_skills(resume_word_list, skill_field, list_of_skill):
    matched_skills = set()

    for skill_name in list_of_skill:
        for word in resume_word_list:
            if re.match('^' + skill_name + '$', word, re.IGNORECASE):
                # if word == 'd':
                #     print skill_name, word
                matched_skills.add(word)
    return matched_skills


def extract_keywords(content):
    wordlist = re.findall(r"[a-zA-Z+#0-9]+", content.lower())
    keyword_list = extract_fields(wordlist)
    # print keyword_list
    return keyword_list


if __name__ == '__main__':
    with open('./uploaded_files/Resume_Yami.txt') as f:
        content = f.read()
    extract_keywords(content)
    # print load_confs()
    # with open('./uploaded_files/Resume_Yami.txt') as f:
    #     content = f.read()
    #     wordlist = re.findall(r"[a-zA-Z+#0-9]+", content.lower())
    #     print extract_fields(wordlist)
