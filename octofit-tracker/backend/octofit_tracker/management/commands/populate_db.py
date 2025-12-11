from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from djongo import models

from octofit_tracker import settings

from django.db import connection

class Command(BaseCommand):
    help = 'Populate the octofit_db database with test data'

    def handle(self, *args, **options):
        User = get_user_model()
        # Delete all data
        User.objects.all().delete()
        self.stdout.write(self.style.SUCCESS('Deleted all users.'))

        # Teams
        from django.apps import apps
        Team = self.get_or_create_model('Team', ['name'])
        Activity = self.get_or_create_model('Activity', ['name', 'user', 'duration', 'date'])
        Leaderboard = self.get_or_create_model('Leaderboard', ['team', 'points'])
        Workout = self.get_or_create_model('Workout', ['name', 'description', 'difficulty'])

        Team.objects.all().delete()
        Activity.objects.all().delete()
        Leaderboard.objects.all().delete()
        Workout.objects.all().delete()
        self.stdout.write(self.style.SUCCESS('Deleted all teams, activities, leaderboard, workouts.'))

        # Create teams
        marvel = Team.objects.create(name='Marvel')
        dc = Team.objects.create(name='DC')

        # Create users
        users = [
            {'username': 'ironman', 'email': 'ironman@marvel.com', 'team': marvel},
            {'username': 'spiderman', 'email': 'spiderman@marvel.com', 'team': marvel},
            {'username': 'batman', 'email': 'batman@dc.com', 'team': dc},
            {'username': 'superman', 'email': 'superman@dc.com', 'team': dc},
        ]
        user_objs = []
        for u in users:
            user = User.objects.create_user(username=u['username'], email=u['email'], password='password')
            user.team = u['team']
            user.save()
            user_objs.append(user)
        self.stdout.write(self.style.SUCCESS('Created users.'))

        # Create activities
        from datetime import datetime, timedelta
        Activity.objects.create(name='Running', user=user_objs[0], duration=30, date=datetime.now())
        Activity.objects.create(name='Cycling', user=user_objs[1], duration=45, date=datetime.now() - timedelta(days=1))
        Activity.objects.create(name='Swimming', user=user_objs[2], duration=60, date=datetime.now() - timedelta(days=2))
        Activity.objects.create(name='Yoga', user=user_objs[3], duration=40, date=datetime.now() - timedelta(days=3))
        self.stdout.write(self.style.SUCCESS('Created activities.'))

        # Create leaderboard
        Leaderboard.objects.create(team=marvel, points=100)
        Leaderboard.objects.create(team=dc, points=90)
        self.stdout.write(self.style.SUCCESS('Created leaderboard.'))

        # Create workouts
        Workout.objects.create(name='Pushups', description='Do 20 pushups', difficulty='Easy')
        Workout.objects.create(name='Plank', description='Hold plank for 1 min', difficulty='Medium')
        Workout.objects.create(name='Burpees', description='Do 10 burpees', difficulty='Hard')
        self.stdout.write(self.style.SUCCESS('Created workouts.'))

        self.stdout.write(self.style.SUCCESS('Database populated successfully.'))

    def get_or_create_model(self, name, fields):
        from django.apps import apps
        try:
            return apps.get_model('octofit_tracker', name)
        except LookupError:
            attrs = {'__module__': 'octofit_tracker.models'}
            for field in fields:
                if field == 'user':
                    attrs[field] = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
                elif field == 'team':
                    attrs[field] = models.ForeignKey('Team', on_delete=models.CASCADE)
                elif field == 'date':
                    attrs[field] = models.DateTimeField()
                elif field == 'duration' or field == 'points':
                    attrs[field] = models.IntegerField()
                else:
                    attrs[field] = models.CharField(max_length=255)
            model = type(name, (models.Model,), attrs)
            return model
