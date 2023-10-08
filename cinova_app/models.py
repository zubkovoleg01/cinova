from django.db import models
from django.contrib.auth.models import User

class Poster(models.Model):
    image = models.ImageField(upload_to='cinova_app/images')
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name
class FavoriteMovie(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movie_id = models.IntegerField()

    def __str__(self):
        return f"{self.user.name} - {self.movie_id}"
