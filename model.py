import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from ast import literal_eval


df_credits=pd.read_csv('tmdb/tmdb_5000_credits.csv')
df_movies=pd.read_csv('tmdb/tmdb_5000_movies.csv')

df_movies=df_movies.drop(columns = ['homepage','budget','production_companies','production_countries','revenue','runtime','status','tagline','original_language','original_title'], axis = 1)
df_credits.columns=['id','title','cast','crew']
df_credits=df_credits.drop(columns=['title'])

df_movies=df_movies.merge(df_credits,on='id')

## Add imdb rating column
# clac mean value
c=df_movies['vote_average'].mean()
# the minimum votes to display
m=df_movies['vote_count'].quantile(0.5)
movies_list=df_movies.copy().loc[df_movies['vote_count']>=m]

def weighted_rating(x,m=m,c=c):
    v=x['vote_count']
    r=x['vote_average']
    return (v/(v+m)*r)+(m/(m+v)*c)

movies_list['score']=movies_list.apply(weighted_rating,axis=1)
movies_list=movies_list.sort_values('score',ascending=False)

## Adjust columns format
features=['genres','keywords','spoken_languages','cast','crew']
for feature in features:
    movies_list[feature]=movies_list[feature].apply(literal_eval)

def get_director(x):
    for i in x:
        if i['job']=='Director':
            return i['name']
        return ''
def get_list(x):
    if isinstance(x,list):
        names=[i['name']for i in x]
        return names
    return []

movies_list['director']=movies_list['crew'].apply(get_director)
features=['genres','keywords','spoken_languages','cast']
for feature in features:
    movies_list[feature]=movies_list[feature].apply(get_list)

movies_list=movies_list.drop(columns=['overview','popularity','vote_average','vote_count','crew'])

## Clean strings
def clean(x):
    if isinstance(x,list):
        return [str.lower(i.replace(" ","")) for i in x]
    
features=['genres','keywords','spoken_languages','cast']
for feature in features:
    movies_list[feature]=movies_list[feature].apply(clean)

# Combine features
def combine(row):
    return ' '.join(row['genres']) + ' ' +' '.join(row['keywords']) + ' ' +' '.join(row['spoken_languages']) + ' ' +' '.join(row['cast'])+' '+row['director']
movies_list['combined']=movies_list.apply(combine,axis=1)

# Counter vector & similarity
count = CountVectorizer(stop_words='english')
count_mat=count.fit_transform(movies_list['combined'])

cosine_sim=cosine_similarity(count_mat,count_mat)
## reset indices
movies_list=movies_list.reset_index()
indices=pd.Series(movies_list.index,index=movies_list['title'])

# get recommendations
def get_rec(title,cosine_sim=cosine_sim):
    if title in movies_list.values :
        idx=indices[title]
        sim_score=list(enumerate(cosine_sim[idx]))
        sim_score=sorted(sim_score,key=lambda x:x[1],reverse =True)
        sim_score=sim_score[1:11]
        movies_indices=[i[0] for i in sim_score]
        return movies_list.iloc[movies_indices]
    return []

