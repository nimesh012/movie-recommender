from django.http import HttpResponse
from django.shortcuts import render
import pickle
import pandas as pd
import requests
from random import sample

movies_df = pd.read_csv('movie_recommender\cleaned_movies_data.csv')
bolly_movies = pd.read_csv(r'movie_recommender\bolly_moviesimg.csv')
sam = pickle.load(open('sam.pkl', 'rb'))
sam_bolly = pickle.load(open('sambolly.pkl', 'rb'))
movies_list = movies_df['title'].values
bolly_title = bolly_movies['title_x'].values

def fetch_poster(id):
    response = requests.get('https://api.themoviedb.org/3/movie/{}?api_key=2bdb67c6db91b990200c89dcda6f68fd'.format(id))
    data = response.json()
    return 'https://image.tmdb.org/t/p/w500'+ data['poster_path']

def fetch_name(id):
    return movies_df[movies_df['movie_id']== id]['title'].tolist()[0]

def fetch_all_poster(id):
    all=[]
    for i in id:
        data= {}
        data['movie_name'] = (fetch_name(i))
        data['movie_poster'] = (fetch_poster(i))
        all.append(data)
    return all



def recommend(movie):
    pred_movie = []
    if movie not in movies_list:
        data = {}
        data['name'] = "movie not found"
        pred_movie.append(data)
        return pred_movie
    else:
        movie_index = movies_df[movies_df['title'] == movie].index[0]
        dist = sam[movie_index]
        movie_list = sorted(list(enumerate(dist)),reverse = True,key = lambda x:x[1])[1:6]
        for i in movie_list:
            data = {}
            data['name'] = movies_df.iloc[i[0]].title
            data['poster'] = fetch_poster(movies_df.iloc[i[0]].movie_id)
            pred_movie.append(data)
        return pred_movie

def hollywood(request):
    movies_img = fetch_all_poster(sample(list(movies_df['movie_id'].values), 10))
    params = {'movies' : movies_img}

    return render(request,'hollywood.html', params)

def bollywood(request):
    params = {'movies':bolly_title}
    return render(request,'bollywood.html', params)

def recommendation(request):
    movie_recommended = request.GET.get('movie','default')
    movies_list = recommend(movie_recommended)
    params = {'movies_listt':movies_list}
    return render(request,'recommendedholly.html',params)

def bolly_recommendation(request):
    movie_recommended = request.GET.get('movie','default')
    movies_list = recom_bollywood(movie_recommended)

    params = {'movies_listt' : movies_list}
    return render(request,'recommended.html',params)

def index(request):
    return render(request,'index.html')



def recom_bollywood(movie):
    pred_movie = []
    if movie not in bolly_title:
        data = {}
        data['name'] = "movie not found"
        pred_movie.append(data)
        return pred_movie

    movie_index = bolly_movies[bolly_movies['title_x'] == movie].index[0]
    dist = sam_bolly[movie_index]
    movie_list = sorted(list(enumerate(dist)), reverse=True, key=lambda x: x[1])[1:6]
    for i in movie_list:
        data = {}
        data['name'] = bolly_movies.iloc[i[0]].title_x
        data['poster'] = bolly_movies.iloc[i[0]].poster_path
        pred_movie.append(data)
    return pred_movie
