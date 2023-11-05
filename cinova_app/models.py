from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinLengthValidator

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

class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    movie_id = models.IntegerField(null=True)
    type_choices = [
        ('positive', 'Положительный'),
        ('negative', 'Отрицательный'),
    ]
    type = models.CharField(max_length=10, choices=type_choices)
    date = models.DateField()
    title = models.CharField(
        max_length=100,
        validators=[MinLengthValidator(limit_value=10, message="Минимальная длина заголовка - 10 символов")]
    )

    review = models.TextField(
        validators=[MinLengthValidator(limit_value=200, message="Минимальная длина отзыва - 200 символов")]
    )

