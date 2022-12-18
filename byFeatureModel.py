import pandas as pd 
import numpy as np
import ast
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from utils.formating import convert,convert2,fetch_director,collapse,toLower

## import datasets 
movies = pd.read_csv('tmdb/tmdb_5000_credits.csv')
credits = pd.read_csv('tmdb/tmdb_5000_movies.csv')
movies = movies.merge(credits,on='title')
movies = movies[['movie_id','title','overview','genres','keywords','cast','crew']]

## cleannig & formatting
movies.dropna(inplace = True)
movies['genres'] = movies['genres'].apply(convert)
movies['keywords'] = movies['keywords'].apply(convert)
movies['cast'] = movies['cast'].apply(convert2)
movies['director'] = movies['crew'].apply(fetch_director)
movies['overview'] = movies['overview'].apply(lambda x : x.split())

    ## collapse
features=['cast','director','genres','keywords']
for feature in features:
    movies[feature]=movies[feature].apply(collapse)
    movies[feature]=movies[feature].apply(toLower)

## merge into single string
movies['tags'] = movies['overview']+movies['genres']+movies['keywords']+movies['cast']+movies['director']

def recommendByFeature(ls):

    new_df = movies[['movie_id','title','tags']]
    l = [12122001,'what user wants']
    l.append(ls)
    new_df.loc[4810] = l
    
    new_df['tags'] = new_df['tags'].apply(lambda x :" ".join(x))
    cv = CountVectorizer(max_features=5000 ,stop_words='english')
    vectors = cv.fit_transform(new_df['tags']).toarray()
    similarity = cosine_similarity(vectors)
    distances = similarity[4806]
    movie_list = sorted(list(enumerate( distances)),reverse =True , key = lambda x:x[1])[1:11]
    
    ans=[]
    for i in movie_list:
        ans.append(new_df.iloc[i[0]].title)
    return ans