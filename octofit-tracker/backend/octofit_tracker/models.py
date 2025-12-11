from djongo import models
from django.contrib.auth.models import AbstractUser
from bson import ObjectId

class Team(models.Model):
    name = models.CharField(max_length=255, unique=True)
    def __str__(self):
        return self.name


class User(AbstractUser):
    id = models.ObjectIdField(primary_key=True, default=ObjectId, editable=False)
    email = models.EmailField(unique=True)
    team = models.ForeignKey(Team, on_delete=models.CASCADE, null=True, blank=True)

class Activity(models.Model):
    name = models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    duration = models.IntegerField()
    date = models.DateTimeField()

class Leaderboard(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    points = models.IntegerField()

class Workout(models.Model):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    difficulty = models.CharField(max_length=50)
