from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
import requests
import asyncio
from django.core.paginator import Paginator
from kinopoisk_dev import KinopoiskDev, MovieField, MovieParams, ReviewField, ReviewParams
from kinopoisk_dev.model import MovieDocsResponseDto, Movie, ReviewDocsResponseDto
from .models import FavoriteMovie, Poster





def home(request):
    posters = Poster.objects.all()
    popular_movies = asyncio.run(get_popular_movies_async())
    new_movies = asyncio.run(get_new_movies_async())
    random_films = [asyncio.run(get_random_async()) for _ in range(4)]

    context = {'popular_movies': popular_movies.docs, 'new_movies': new_movies.docs, 'posters': posters,
               'random_films': random_films}

    return render(request, 'cinova_app/home.html', context)

def custom_404(request, exception):
    return render(request, '404.html', status=404)


@login_required
def likes_view(request):
    user = request.user
    favorite_movies = FavoriteMovie.objects.filter(user=user)

    movies_info = []

    for favorite_movie in favorite_movies:
        kp = KinopoiskDev(token=TOKEN)
        movie = kp.find_one_movie(favorite_movie.movie_id)

        movies_info.append({
            'movie_id': favorite_movie.movie_id,
            'movie_info': movie
        })

    context = {'movies_info': movies_info}

    return render(request, 'cinova_app/likes.html', context)

def thank_you(request):
    return render(request, 'cinova_app/thank_you.html')

@login_required
def account_view(request):
    return render(request, 'account/account.html' )

def movie_view(request):
    kp = KinopoiskDev(token=TOKEN)
    page_number = request.GET.get('page', 1)
    item = kp.find_many_movie(
        params=[
            MovieParams(keys=MovieField.PAGE, value=page_number),
            MovieParams(keys=MovieField.LIMIT, value=16),
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
        API_KEY = ""
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
            MovieParams(keys=MovieField.LIMIT, value=30),
            MovieParams(keys=MovieField.TYPE, value='movie'),
        ]
    )

    return item

async def get_new_movies_async() -> MovieDocsResponseDto:
    kp = KinopoiskDev(token=TOKEN)
    item = await kp.afind_many_movie(
        params=[
            MovieParams(keys=MovieField.PAGE, value=1),
            MovieParams(keys=MovieField.LIMIT, value=30),
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


def filtered_movies(request, genre):
    headers = {"X-API-KEY": TOKEN}

    url = 'https://api.kinopoisk.dev/v1/movie'
    params = {
        "genres.name": genre,
        "limit": request.GET.get('limit', 32),
        "page": request.GET.get('page', 1),
    }

    response = requests.get(url, params=params, headers=headers)
    movies = response.json().get('docs', [])

    paginator = Paginator(movies, 16)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)

    context = {'movies': page_obj, 'genre': genre, 'page_obj': page_obj}
    return render(request, 'cinova_app/filtered_movies.html', context)

def get_review(request, movie_id) -> ReviewDocsResponseDto:
    kp = KinopoiskDev(token=TOKEN)
    item = kp.review(
        params=[
            ReviewParams(keys=ReviewField.MOVIE_ID, value=movie_id),
            ReviewParams(keys=ReviewField.PAGE, value=1),
            ReviewParams(keys=ReviewField.LIMIT, value=10),
        ]
    )
    reviews = item
    return render(request, 'cinova_app/reviews.html', {'reviews': reviews})



