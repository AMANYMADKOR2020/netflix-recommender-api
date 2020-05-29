import pandas as pd
import numpy as np
import os
#import spacy
from string import punctuation
from sklearn.metrics.pairwise import cosine_similarity
#from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.pipeline import Pipeline
import joblib



#nlp=spacy.load("en_core_web_md")
df_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "netflix_titles.csv")
PICKLES_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "pickles")

# if the folder doesn't exist
if not os.path.exists(PICKLES_PATH):
    os.mkdir(PICKLES_PATH)
df= pd.read_csv(df_path)
new_df = df.loc[:,('title','director','cast','listed_in','description')]
new_df['newdescription'] = df['description'].fillna('')+' '+df['cast'].fillna('')  + ' '+df['listed_in'].fillna('')+' '+df['director'].fillna('')  
new_df_fin=new_df.loc[:,('title','newdescription')]
new_df_fin.set_index('title', inplace = True)
indices = pd.Series(new_df_fin.index)
def train():      
    tfidf = TfidfVectorizer(stop_words='english')
    tfidf_matrix = tfidf.fit_transform(new_df_fin['newdescription'])
        
    cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)
        # export the model
    cos_path = os.path.join(PICKLES_PATH, "cos.pkl")
    joblib.dump(cosine_sim, cos_path, compress=True)
        
def load_cos():
    cos_path = os.path.join(PICKLES_PATH, "cos.pkl")
    if os.path.exists(cos_path):
        return joblib.load(cos_path)
    else:
        return None

# function that takes in movie title as input and returns the top 10 recommended movies
def recommendations(Title, cosine_sim = load_cos()):
    
    recommended_movies = []
    title ={}
    # gettin the index of the movie that matches the title
    idx = indices[indices == Title].index[0]

    # creating a Series with the similarity scores in descending order
    score_series = pd.Series(cosine_sim[idx]).sort_values(ascending = False)
    top_5= list(score_series.iloc[1:6])
    # getting the indexes of the 5 most similar movies
    top_5_indexes = list(score_series.iloc[1:6].index)
    
    # populating the list with the titles of the best 5 matching movies
    s=0
    for i in top_5_indexes:
        title={"title":(new_df_fin.index)[i],
               "confidence":round(top_5[s],2)}
        recommended_movies.append(title)
        s=s+1
    return recommended_movies

if __name__ == "__main__":
     recommendations("Rocky", load_cos() )