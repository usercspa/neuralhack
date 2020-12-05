import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.feature_extraction.text import TfidfVectorizer, ENGLISH_STOP_WORDS
from sklearn.pipeline import make_pipeline
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans, MiniBatchKMeans
from sklearn.manifold import TSNE
from sklearn.decomposition import TruncatedSVD 
from sklearn.preprocessing import normalize 
from make_csv import *

emails = pd.read_csv('email_dataset.csv')
dataframe = pd.DataFrame(parse_into_emails(emails.message))
dataframe.drop(dataframe.query("body == '' | to == '' | from_ == ''").index, inplace=True)
stopwords = ENGLISH_STOP_WORDS.union([ 'hou', 'com', 'recipient'])
vect = TfidfVectorizer(analyzer='word', stop_words=stopwords, max_df=0.6, min_df=2)

X = vect.fit_transform(dataframe.body)
features = vect.get_feature_names()

n_clusters = 3
clf = KMeans(n_clusters=n_clusters,max_iter=100,init='k-means++', n_init=1)
labels = clf.fit_predict(my_email.csv)	
clusters = {}
    n = 0
    for item in labels:
        if item in clusters:
            clusters[item].append(row_dict[n])
        else:
            clusters[item] = [row_dict[n]]
        n +=1
