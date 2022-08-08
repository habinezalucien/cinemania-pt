from django.db import models
from django.contrib.auth.models import AbstractUser

# Create 'Users' model
class User(AbstractUser):
    sex = (('M', 'Male'), ('F', 'Female'), ('O', 'Other'))
    gender = models.CharField(max_length=10, choices=sex, default='M')
    age = models.IntegerField(null=True, blank=True)
    profile_image = models.FileField(upload_to = 'images/', null=True, blank=True)
        
    
# Create 'Movies' model 
class Movie(models.Model):
    type = (('G', 'General'), ('A', 'Adults'), ('K', 'Kids'))
    title = models.CharField(max_length=255)
    release_date = models.DateField()
    main_actors = models.CharField(max_length=255 ,null=True)
    genre = models.CharField(max_length=100)
    movie_type = models.CharField(max_length=100, choices=type, default='G')
    description = models.CharField(max_length=255)
    poster = models.ImageField(upload_to = 'images/', null=True,  blank=True)
    trailer_link = models.URLField(max_length=255, null=True)
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE)
    uploaded_on = models.DateTimeField()
    movie = models.FileField(upload_to = 'movies/')
    
    def __str__(self):
        return f"{self.title} of {self.release_date}"
    
class Activity(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    action = models.CharField(max_length=255)
    time = models.DateTimeField()
    
    def __str__(self):
        return f"{self.user} {self.action}"
    
class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    comment = models.CharField(max_length=255)
    
    def __str__(self):
        return f"{self.user} of {self.movie}"
    
# Create 'Favorite Movies' model
class Favorite_Movie(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.movie} {self.user}"
    
class watch_list(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.movie} {self.user}"
    