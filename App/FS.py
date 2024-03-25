
import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
def forcastability_score_cosine_with_rep(feature_vector):
    representative=pd.read_json('/home/codit/PycharmProjects/DataGenie-Hackathon/Prophet Data/representative.json',typ='series')
    representative=pd.DataFrame(representative)
    rep=representative.iloc[:,0].tolist()
    rep = np.array(rep).reshape(1,-1)
    feature_vector = np.array(feature_vector).reshape(1,-1)
    similarity = cosine_similarity(rep,feature_vector)[0][0]
    similarity = 5*(similarity+1)
    return similarity