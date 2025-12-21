from django.db import models

class Genre(models.Model):
    name = models.CharField(max_length=100)

class Director(models.Model):
    name = models.CharField(max_length=100)

class Actor(models.Model):
    name = models.CharField(max_length=100)

class Movie(models.Model):
    title = models.CharField(max_length=200)
    year = models.IntegerField()
    imdb_score = models.FloatField()
    votes = models.IntegerField()
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)
    director = models.ForeignKey(Director, on_delete=models.CASCADE)
    actors = models.ManyToManyField(Actor)
