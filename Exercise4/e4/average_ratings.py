import numpy as np
import pandas as pd
import sys
import difflib
import csv

movie_list = sys.argv[1]
ratings = sys.argv[2]
output = sys.argv[3]

movies = open(movie_list).readlines()
df = pd.DataFrame(movies, columns={'title'})
movies_series = df['title'].str.replace('\n','', regex=True)
movies_df = pd.DataFrame(movies_series, columns={'title'})

def match_title(title):
    match = difflib.get_close_matches(title, movies_df['title'], n=1, cutoff=0.6)
    return match

movie_ratings = pd.read_csv(ratings)
ratings_df = pd.DataFrame(movie_ratings, columns=['title', 'rating'])
matched_ratings = ratings_df['title'].apply(lambda title:match_title(title))
ratings_df['matched'] = matched_ratings
ratings_df['matched'] = ratings_df['matched'].astype(str)
ratings_df['matched'] = ratings_df['matched'].str.strip('["]')
ratings_df['matched'] = ratings_df['matched'].str.strip("'")
ratings_df = ratings_df[ratings_df.matched != '']

ratings_df = ratings_df.drop('title',1)
ratings_df = ratings_df.rename(columns={"matched":"title"})
ratings_df = ratings_df.reindex(columns=["title","rating"])

ratings_df = ratings_df.groupby(['title']).mean()
ratings_df['rating'] = ratings_df['rating'].round(2)
ratings_df.to_csv(output)