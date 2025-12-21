import pandas as pd
from django.core.management.base import BaseCommand
from movies_app.models import Movie, Genre, Director, Actor

def safe_int(value):
    try:
        return int(value)
    except (ValueError, TypeError):
        return None

def safe_float(value):
    try:
        return float(value)
    except (ValueError, TypeError):
        return None

class Command(BaseCommand):
    help = 'Load movies from CSV'

    def handle(self, *args, **kwargs):
        self.stdout.write('Начинаю загрузку фильмов...')

        df = pd.read_csv('movies.csv').head(7000)  # берем только первые 7000 строк
        df = df.dropna(subset=['name'])            # удаляем полностью пустые строки

        for i, row in df.iterrows():
            genre, _ = Genre.objects.get_or_create(name=row['genre'])
            director, _ = Director.objects.get_or_create(name=row['director'])

            movie = Movie.objects.create(
                title=row['name'],
                year=safe_int(row['year']),
                imdb_score=safe_float(row['score']),
                votes=safe_int(row['votes']),
                genre=genre,
                director=director
            )

            for actor in str(row['star']).split(','):
                actor_obj, _ = Actor.objects.get_or_create(name=actor.strip())
                movie.actors.add(actor_obj)

            if i % 100 == 0:
                self.stdout.write(f'Загружено {i} фильмов')

        self.stdout.write(self.style.SUCCESS('Загрузка фильмов завершена'))
