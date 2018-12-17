import pandas
import re


exp_pattern_list = ['experience']
string_numbers = {'one':1, 'two':2, 'three':3, 'four':4, 'five':5, 'six':6, 'seven':7, 'eight':8, 'nine': 9}

def load_jd_data(data_file = 'data.csv'):
    jds = pandas.read_csv(data_file)
    return jds

def get_all_exp_require():
    jds = load_jd_data()
    jds["exp_req"] = jds["Job Description"].apply(lambda x:_apply_search_exp_require(x))
    return jds

def exp_req_filter(jds = None, low_bound = 0, high_bound = 0):
    try:
        if not jds:
            jds = load_jd_data()
            jds = get_all_exp_require()
        print jds['exp_req'].apply(lambda x:_apply_is_meet_exp_req(x, low_bound))
        filtered_jds = jds[jds['exp_req'].apply(lambda x:_apply_is_meet_exp_req(x, low_bound))]
        return filtered_jds
    except:
        return

def _apply_is_meet_exp_req(list, low_bound):
    is_meet_req = False
    if low_bound >= list[0]:
        is_meet_req = True
    return is_meet_req

def _apply_search_exp_require(string):
    lines = [line for line in string.split('\n') if line]
    # print lines

    exp_range = [0, 10]
    for line in lines:
        for pattern in exp_pattern_list:
            if re.search(pattern, line, re.IGNORECASE):
                exp_range = merge_range(exp_range, extract_range(line))
    return [exp_range[0], exp_range[0]+0.5]

def extract_range(string):
    exp_range = [0, 10]
    count = 0
    for num in string_numbers.keys():
        if re.search(num, string, re.IGNORECASE):
            if count < 2:
                exp_range[count] = string_numbers[num]
            count += 1

    for num in range(10):
        if re.search(str(num) + '[+-]?', string):
            if count < 2 :
                exp_range[count] = num
            count += 1

    return exp_range

def merge_range(a, b):
    try:
        exp_range = [max(a[0], b[0]), min(a[1], b[1])]
        if exp_range[0] > exp_range[1]:
            if a[1] < b[0]:
                exp_range = b.copy()
            elif b[1] < a[0]:
                exp_range = a.copy()
        exp_range = [min(10, exp_range[0]), min(10, exp_range[1])]
        return exp_range
    except:
        return [0, 10]

if __name__ == '__main__':
    load_jd_data()
    with open('test_exp.txt') as f:
        content = f.read()
    # print _apply_search_exp_require(content)
    # print extract_range('2-5 experience')
    print exp_req_filter()
