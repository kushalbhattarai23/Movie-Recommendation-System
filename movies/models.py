from django.db import models
from django.contrib.auth.models import User
import csv
import os
from datetime import datetime

class PasswordResetToken(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    token = models.CharField(max_length=32, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Password reset token for {self.user.username}"
        
       
class Cinema(models.Model):
    id = models.AutoField(primary_key=True)
    tmdbId = models.IntegerField()
    original_language = models.CharField(max_length=100)
    title = models.CharField(max_length=200)
    original_title = models.CharField(max_length=200)
    overview = models.TextField()
    poster_path = models.CharField(max_length=200)
    tagline = models.CharField(max_length=200)
    keywords = models.TextField()
    release_date = models.CharField(max_length=100)
    genres = models.TextField()

    def __str__(self):
        return self.title


class MovieRating(models.Model):
    id = models.AutoField(primary_key=True)
    userId = models.CharField(max_length=200)
    movieId = models.CharField(max_length=200)
    rating = models.CharField(max_length=200)
    timestamp = models.CharField(max_length=200)
