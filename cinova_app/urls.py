from django.urls import path
from . import views


app_name = 'cinova'

urlpatterns = [
    path('movies/', views.movie_view, name='movies'),
    path('movies/<int:movie_id>/', views.movie_detail, name='movie_detail'),
    path('series/', views.series_view, name='series'),
    path('series/<int:series_id>/', views.series_detail, name='series_detail'),
    path('account/', views.account_view, name='account'),
    path('likes/', views.likes_view, name='likes'),
    path('likes/<int:movie_id>/', views.add_to_favorites, name='add_to_favorites'),
    path('likes/remove/<int:movie_id>/', views.remove_from_favorites, name='remove_from_favorites'),
    path('search_movies/', views.search_movies, name='search_movies'),
]
