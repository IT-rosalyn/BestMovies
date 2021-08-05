from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User
# Create your models here.
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    website = models.URLField(blank=True)
    picture = models.ImageField(upload_to='profile_images', blank=True)

    def __str__(self):
        return self.user.username

class Movie(models.Model):
        name = models.CharField(max_length=128, unique=True)
        category = models.CharField(max_length=128)
        average_rating = models.FloatField(default=0)
        slug = models.SlugField(unique=True)
        description = models.CharField(max_length=128)
        img = models.ImageField(upload_to='profile_images', default='profile_images/default.png')
        genre = models.CharField(max_length=128)
        actor = models.CharField(max_length=128)
        director = models.CharField(max_length=128)
        date = models.DateField()
        launage = models.CharField(max_length=128)
        Production_country = models.CharField(max_length=128)
        people=models.IntegerField(default=0)
        def save(self, *args, **kwargs):
            self.slug = slugify(self.name)
            super(Movie, self).save(*args, **kwargs)

        def __str__(self):
            return self.name

class FavoriteList(models.Model):
        user = models.OneToOneField(User, on_delete=models.CASCADE)
        movie = models.CharField(validators=[],max_length=200)

        def __str__(self):
            return self.user.username



class Review(models.Model):
        title = models.CharField(max_length=128)
        user = models.ForeignKey(User, on_delete=models.CASCADE)
        movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
        content = models.CharField(max_length=128)
        date = models.DateField()
        dislike = models.PositiveIntegerField(default=0)
        like = models.PositiveIntegerField(default=0)
        # rate to  movie
        rating = models.PositiveIntegerField(default=1)
        status=models.IntegerField(default=0)
        def __str__(self):
            return self.title
        class Meta:
            ordering=('-date',)
