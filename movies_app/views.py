from django.shortcuts import render
from movies_app.models import Movie, Genre, Director
from django.db.models import Count, Avg
from django.shortcuts import render, redirect, get_object_or_404
from .models import Movie
from .forms import MovieForm

def movie_list(request):
    movies = Movie.objects.all()
    return render(request, 'movie_list.jinja', {'movies': movies})


def movie_create(request):
    if request.method == 'POST':
        form = MovieForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('movie_list')
    else:
        form = MovieForm()
    return render(request, 'movie_form.jinja', {'form': form})


def movie_update(request, pk):
    movie = get_object_or_404(Movie, pk=pk)
    if request.method == 'POST':
        form = MovieForm(request.POST, instance=movie)
        if form.is_valid():
            form.save()
            return redirect('movie_list')
    else:
        form = MovieForm(instance=movie)
    return render(request, 'movie_form.jinja', {'form': form})


def movie_delete(request, pk):
    movie = get_object_or_404(Movie, pk=pk)
    if request.method == 'POST':
        movie.delete()
        return redirect('movie_list')
    return render(request, 'movie_confirm_delete.jinja', {'movie': movie})


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
