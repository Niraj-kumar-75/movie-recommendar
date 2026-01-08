import streamlit as st
import pandas as pd
import pickle
import requests


# from package_name.beta_columns import beta_columns


def fetch_poster(movie):
    response = requests.get(
        url = "https://api.themoviedb.org/3/movie/{}?api_key=4e261c4223980efcab0725ec3e85a696".format(
            movie))
    data = response.json()
    return "https://image.tmdb.org/t/p/w500/" + data['poster_path']




api_key = st.secrets["TMDB_API_KEY"]

def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={api_key}"
    data = requests.get(url).json()

    poster_path = data.get('poster_path')
    if poster_path:
        return "https://image.tmdb.org/t/p/w500/" + poster_path
    else:
        return "https://via.placeholder.com/500x750?text=No+Poster"


def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]

    movie_list = sorted(
        list(enumerate(distances)),
        reverse=True,
        key=lambda x: x[1]
    )[1:6]

    recommend_movie = []
    recommend_movie_poster = []

    for i in movie_list:
        movie_id = movies.iloc[i[0]]['id']
        recommend_movie.append(movies.iloc[i[0]]['title'])
        recommend_movie_poster.append(fetch_poster(movie_id))

    return recommend_movie, recommend_movie_poster


# 🔥 LOAD DATA
movies = pickle.load(open('movies.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))

# 🔥 STREAMLIT UI
st.title("🎬 Movie Recommender System")

option = st.selectbox(
    "Select a movie",
    movies['title'].values
)

if st.button("Recommend"):
    names, posters = recommend(option)

    cols = st.columns(5)
    for i in range(5):
        with cols[i]:
            st.text(names[i])
            st.image(posters[i])

