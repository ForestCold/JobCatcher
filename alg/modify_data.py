import pandas as pd
import os
import sys
import pickle
from match_tfidf import train

reload(sys)
sys.setdefaultencoding('utf8')

# df = pd.read_csv("naukri_com-job_sample.csv")
# for i, trial in df.iterrows():
#     if i%100==0:
#         print i
#     df.loc[i, "jobdescription"] = str(df.loc[i, "jobdescription"]).replace("Job Description   Send me Jobs like this","")
#
# df.to_csv("naukri.csv")
# print df

tf, tfidf, df = train("naukri.csv")
with open('tf.pickle', 'wb') as handle:
    pickle.dump(tf, handle, protocol=pickle.HIGHEST_PROTOCOL)
with open('tfidf.pickle', 'wb') as handle:
    pickle.dump(tfidf, handle, protocol=pickle.HIGHEST_PROTOCOL)
with open('df.pickle', 'wb') as handle:
    pickle.dump(df, handle, protocol=pickle.HIGHEST_PROTOCOL)
# print df