from django.shortcuts import render
from movies_app.models import Movie, Genre, Director
from django.db.models import Count, Avg


def index(request):
    # Основные данные
    movies = Movie.objects.all().select_related('genre', 'director')

    # Статистика по жанрам
    genre_stats = Genre.objects.annotate(
        movie_count=Count('movie'),
        avg_score=Avg('movie__imdb_score')
    ).order_by('-movie_count')

    # Статистика по режиссерам
    director_stats = Director.objects.annotate(
        movie_count=Count('movie')
    ).order_by('-movie_count')[:10]

    context = {
        'movies': movies,
        'genre_stats': genre_stats,
        'director_stats': director_stats,
    }

    return render(request, 'movies_app/index.jinja2', context, using='jinja')