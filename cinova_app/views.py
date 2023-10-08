from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.core.mail import send_mail
import requests
import asyncio
from typing import List
from django.core.paginator import Paginator
from kinopoisk_dev import KinopoiskDev, MovieField, MovieParams, SeasonField, SeasonParams, PossValField
from kinopoisk_dev.model import MovieDocsResponseDto, Movie, SeasonDocsResponseDto, PossibleValue
from .models import FavoriteMovie, Poster


TOKEN = "YOUR TOKEN"

def home(request):
    posters = Poster.objects.all()
    popular_movies = asyncio.run(get_popular_movies_async())
    new_movies = asyncio.run(get_new_movies_async())
    action_movies = asyncio.run(get_action_movies_async())

    return render(request, 'cinova_app/home.html', {'popular_movies': popular_movies.docs, 'new_movies': new_movies.docs, 'action_movies': action_movies.docs, 'posters': posters})
@login_required
def likes_view(request):
    user = request.user
    favorite_movies = FavoriteMovie.objects.filter(user=user)
    return render(request, 'cinova_app/likes.html', {'favorite_movies': favorite_movies})

@login_required
def account_view(request):
    return render(request, 'accounts/account.html')

def movie_view(request):
    kp = KinopoiskDev(token=TOKEN)
    item = kp.find_many_movie(
        params=[
            MovieParams(keys=MovieField.PAGE, value=3),
            MovieParams(keys=MovieField.LIMIT, value=16),
            MovieParams(keys=MovieField.TYPE, value='movie'),
        ]
    )

    movies = item
    return render(request, 'cinova_app/movies.html', {'movies': movies})

def series_view(request) -> MovieDocsResponseDto:
    kp = KinopoiskDev(token=TOKEN)
    item = kp.find_many_movie(
        params=[
            MovieParams(keys=MovieField.PAGE, value=2),
            MovieParams(keys=MovieField.LIMIT, value=16),
            MovieParams(keys=MovieField.TYPE, value='tv-series'),
        ]
    )
    series = item
    return render(request, 'cinova_app/series.html', {'series': series})

def search_movies(request):
    query = request.GET.get('q', '')

    if query:
        API_KEY = "8c8e1a50-6322-4135-8875-5d40a5420d86"
        API_URL_SEARCH = f"https://kinopoiskapiunofficial.tech/api/v2.1/films/search-by-keyword?keyword={query}"
        response = requests.get(API_URL_SEARCH, headers={"X-API-KEY": API_KEY})
        movies_data = response.json().get('films', [])
    else:
        movies_data = []

    context = {'movies_data': movies_data}
    return render(request, 'cinova_app/search_result.html', context)

def movie_detail(request, movie_id):
    kp = KinopoiskDev(token=TOKEN)
    movie = kp.find_one_movie(movie_id)
    return render(request, 'cinova_app/movie_detail.html', {'movie': movie})

def series_detail(request, series_id):
    kp = KinopoiskDev(token=TOKEN)
    series = kp.find_one_movie(series_id)
    return render(request, 'cinova_app/series_detail.html', {'series': series})

async def get_popular_movies_async() -> MovieDocsResponseDto:
    kp = KinopoiskDev(token=TOKEN)
    item = await kp.afind_many_movie(
        params=[
            MovieParams(keys=MovieField.PAGE, value=1),
            MovieParams(keys=MovieField.LIMIT, value=4),
            MovieParams(keys=MovieField.TYPE, value='movie'),
        ]
    )
    return item

async def get_new_movies_async() -> MovieDocsResponseDto:
    kp = KinopoiskDev(token=TOKEN)
    item = await kp.afind_many_movie(
        params=[
            MovieParams(keys=MovieField.PAGE, value=1),
            MovieParams(keys=MovieField.LIMIT, value=4),
            MovieParams(keys=MovieField.TYPE, value='movie'),
            MovieParams(keys=MovieField.YEAR, value='2023'),
        ]
    )
    return item

async def get_action_movies_async() -> MovieDocsResponseDto:
    kp = KinopoiskDev(token=TOKEN)
    item = await kp.afind_many_movie(
        params=[

            MovieParams(keys=MovieField.PAGE, value=1),
            MovieParams(keys=MovieField.LIMIT, value=4),
            MovieParams(keys=MovieField.TYPE, value='movie'),
            MovieParams(keys=MovieField.SELECT_FIELDS, value='боевик'),
        ]

    )
    return item

def add_to_favorites(request, movie_id):

    user = request.user
    favorite_movies = FavoriteMovie.objects.filter(user=user, movie_id=movie_id)

    # If there are no matching records, create one.
    if not favorite_movies.exists():
        favorite_movie = FavoriteMovie(user=user, movie_id=movie_id)
        favorite_movie.save()
    return redirect('cinova:likes')

def remove_from_favorites(request, movie_id):
    user = request.user
    favorite_movie = FavoriteMovie.objects.filter(user=user, movie_id=movie_id).first()

    if favorite_movie:
        favorite_movie.delete()
    else:
        print(f"No favorite movie found with id {movie_id}")

    return redirect('cinova:likes')