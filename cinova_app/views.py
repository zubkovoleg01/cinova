from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
import requests
import asyncio
from django.utils import timezone
from django.core.paginator import Paginator
from kinopoisk_dev import KinopoiskDev, MovieField, MovieParams, ReviewField, ReviewParams
from kinopoisk_dev.model import MovieDocsResponseDto, Movie, ReviewDocsResponseDto
from .models import FavoriteMovie, Poster, Comment
from .forms import CommentForm

TOKEN = "YOUR TOKEN"

def home(request):
    posters = Poster.objects.all()
    popular_movies = asyncio.run(get_popular_movies_async())
    new_movies = asyncio.run(get_new_movies_async())
    random_films = [asyncio.run(get_random_async()) for _ in range(4)]

    context = {'popular_movies': popular_movies.docs, 'new_movies': new_movies.docs, 'posters': posters,
               'random_films': random_films}

    return render(request, 'cinova_app/home.html', context)

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

@login_required
def account_view(request):
    user_comments = Comment.objects.filter(author=request.user).order_by('-date')
    context = {'user_comments': user_comments}
    return render(request, 'account/account.html', context)


def movie_view(request):
    kp = KinopoiskDev(token=TOKEN)
    page_number = request.GET.get('page', 1)
    item = kp.find_many_movie(
        params=[
            MovieParams(keys=MovieField.PAGE, value=page_number),
            MovieParams(keys=MovieField.LIMIT, value=9999),
            MovieParams(keys=MovieField.TYPE, value='movie'),
        ]
    )
    movies = item.docs

    paginator = Paginator(movies, 20)
    page_obj = paginator.get_page(page_number)

    context = {'page_obj': page_obj}

    return render(request, 'cinova_app/movies.html', context)


def series_view(request):
    kp = KinopoiskDev(token=TOKEN)
    page_number = request.GET.get('page', 1)
    item = kp.find_many_movie(
        params=[
            MovieParams(keys=MovieField.PAGE, value=page_number),
            MovieParams(keys=MovieField.LIMIT, value=9999),
            MovieParams(keys=MovieField.TYPE, value='tv-series'),
        ]
    )

    series = item.docs

    paginator = Paginator(series, 20)
    page_obj = paginator.get_page(page_number)

    context = {'series': series, 'page_obj': page_obj}

    return render(request, 'cinova_app/series.html', context)

def search_movies(request):
    query = request.GET.get('q', '')

    if query:
        API_KEY = "YOUR TOKEN"
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

    context = {'series': series}

    return render(request, 'cinova_app/series_detail.html', context)

async def get_popular_movies_async() -> MovieDocsResponseDto:
    kp = KinopoiskDev(token=TOKEN)
    item = await kp.afind_many_movie(
        params=[
            MovieParams(keys=MovieField.PAGE, value=1),
            MovieParams(keys=MovieField.LIMIT, value=100),
            MovieParams(keys=MovieField.TYPE, value='movie'),
        ]
    )

    return item

async def get_new_movies_async() -> MovieDocsResponseDto:
    kp = KinopoiskDev(token=TOKEN)
    item = await kp.afind_many_movie(
        params=[
            MovieParams(keys=MovieField.PAGE, value=1),
            MovieParams(keys=MovieField.LIMIT, value=100),
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
        "limit": request.GET.get('limit', 9999),
        "page": request.GET.get('page', 1),
    }

    response = requests.get(url, params=params, headers=headers)
    movies = response.json().get('docs', [])

    paginator = Paginator(movies, 20)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)

    context = {'movies': page_obj, 'genre': genre, 'page_obj': page_obj}

    return render(request, 'cinova_app/filtered_movies.html', context)

def get_review(request, movie_id) -> ReviewDocsResponseDto:
    kp = KinopoiskDev(token=TOKEN)
    page_number = request.GET.get('page', 1)
    item = kp.review(
        params=[
            ReviewParams(keys=ReviewField.MOVIE_ID, value=movie_id),
            MovieParams(keys=MovieField.PAGE, value=page_number),
            ReviewParams(keys=ReviewField.LIMIT, value=100),
        ]
    )
    reviews = item.docs

    reviews_from_site = Comment.objects.filter(movie_id=movie_id).order_by('-date')

    paginator = Paginator(reviews, 10)
    page_obj = paginator.get_page(page_number)

    context = {'reviews': reviews, 'page_obj': page_obj, 'reviews_from_site': reviews_from_site}

    return render(request, 'cinova_app/reviews.html', context)

def add_review(request, movie_id):
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.date = timezone.now()
            comment.movie_id = movie_id
            comment.save()
            return redirect('cinova:reviews', movie_id)
    else:
        form = CommentForm()

    context = {'form': form, 'movie_id': movie_id}

    return render(request, 'cinova_app/add_review.html', context)

def delete_review(request, movie_id):
    reviews_from_site = Comment.objects.filter(movie_id=movie_id, author=request.user)
    if reviews_from_site.exists():
        review_to_delete = reviews_from_site[0]
        review_to_delete.delete()

    return redirect('cinova:account')
