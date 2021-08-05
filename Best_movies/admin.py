from django.contrib import admin
from Best_movies.models import Movie,FavoriteList,UserProfile,Review
# Register your models here.

admin.site.register(UserProfile)
admin.site.register(Movie)
admin.site.register(Review)
admin.site.register(FavoriteList)
