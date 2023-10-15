from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
import requests
import asyncio
from django.core.paginator import Paginator
from kinopoisk_dev import KinopoiskDev, MovieField, MovieParams
from kinopoisk_dev.model import MovieDocsResponseDto, Movie
from .models import FavoriteMovie, Poster


TOKEN = "YOUR_TOKEN"


def home(request):
    posters = Poster.objects.all()
    popular_movies = asyncio.run(get_popular_movies_async())
    new_movies = asyncio.run(get_new_movies_async())
    random_film = asyncio.run(get_random_async())

    context = {'popular_movies': popular_movies.docs, 'new_movies': new_movies.docs, 'posters': posters, 'random_film': random_film}

    return render(request, 'cinova_app/home.html', context)

def custom_404(request, exception):
    return render(request, '404.html', status=404)

@login_required
def likes_view(request):
    user = request.user
    favorite_movies = FavoriteMovie.objects.filter(user=user)
    context = {'favorite_movies': favorite_movies}

    return render(request, 'cinova_app/likes.html', context)


@login_required
def account_view(request):
    return render(request, 'account/account.html')

def movie_view(request):
    kp = KinopoiskDev(token=TOKEN)
    page_number = request.GET.get('page', 1)
    item = kp.find_many_movie(
        params=[
            MovieParams(keys=MovieField.PAGE, value=page_number),
            MovieParams(keys=MovieField.LIMIT, value=8),
            MovieParams(keys=MovieField.TYPE, value='movie'),
        ]
    )
    movies = item.docs

    paginator = Paginator(movies, 4)
    page_obj = paginator.get_page(page_number)

    return render(request, 'cinova_app/movies.html', {'movies': movies, 'page_obj': page_obj})


def series_view(request):
    kp = KinopoiskDev(token=TOKEN)
    page_number = request.GET.get('page', 1)
    item = kp.find_many_movie(
        params=[
            MovieParams(keys=MovieField.PAGE, value=page_number),
            MovieParams(keys=MovieField.LIMIT, value=16),
            MovieParams(keys=MovieField.TYPE, value='tv-series'),
        ]
    )

    series = item.docs

    paginator = Paginator(series, 4)
    page_obj = paginator.get_page(page_number)

    return render(request, 'cinova_app/series.html', {'series': series, 'page_obj': page_obj})

def search_movies(request):
    query = request.GET.get('q', '')

    if query:
        API_KEY = "YOUR_TOKEN"
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

    context = {'movie': movie}
    return render(request, 'cinova_app/movie_detail.html', context)


def series_detail(request, series_id):
    kp = KinopoiskDev(token=TOKEN)
    series = kp.find_one_movie(series_id)

    return render(request, 'cinova_app/series_detail.html', {'series': series})

async def get_popular_movies_async() -> MovieDocsResponseDto:
    kp = KinopoiskDev(token=TOKEN)
    item = await kp.afind_many_movie(
        params=[
            MovieParams(keys=MovieField.PAGE, value=1),
            MovieParams(keys=MovieField.LIMIT, value=17),
            MovieParams(keys=MovieField.TYPE, value='movie'),
        ]
    )

    return item

async def get_new_movies_async() -> MovieDocsResponseDto:
    kp = KinopoiskDev(token=TOKEN)
    item = await kp.afind_many_movie(
        params=[
            MovieParams(keys=MovieField.PAGE, value=1),
            MovieParams(keys=MovieField.LIMIT, value=17),
            MovieParams(keys=MovieField.TYPE, value='movie'),
            MovieParams(keys=MovieField.YEAR, value='2023'),
        ]
    )

    return item

@login_required
def add_to_favorites(request, movie_id):

    user = request.user
    favorite_movies = FavoriteMovie.objects.filter(user=user, movie_id=movie_id)

    if not favorite_movies.exists():
        favorite_movie = FavoriteMovie(user=user, movie_id=movie_id)
        favorite_movie.save()

    return redirect('cinova:likes')

@login_required
def remove_from_favorites(request, movie_id):
    user = request.user
    favorite_movie = FavoriteMovie.objects.filter(user=user, movie_id=movie_id).first()

    if favorite_movie:
        favorite_movie.delete()
    else:
        print(f"No favorite movie found with id {movie_id}")

    return redirect('cinova:likes')

async def get_random_async() -> Movie:
    kp = KinopoiskDev(token=TOKEN)
    item = await kp.arandom()
    return item



