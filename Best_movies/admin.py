from django.contrib import admin
from rango.models import Movie, FavoriteList, UserProfile,Review,
# Register your models here.
admin.site.register(Category)
admin.site.register(Page)
admin.site.register(UserProfile)
admin.site.register(Movie)
admin.site.register(Review)
admin.site.register(FavoriteList)
