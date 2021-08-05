from django.urls import path
from rango import views

app_name='Best_movies'
urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('search/', views.search, name='search'),
    path('detail/<slug:name>/', views.detail, name='detail'),
    path('detail/<slug:name>/<int:id>/like/', views.like, name='like'),
    path('detail/<slug:name>/<int:id>/dislike/', views.dislike, name='dislike'),
    path('detail/<slug:name>/<str:username>/add_review/', views.add_review, name='add_review'),
    path('<str:username>/favorite/', views.favorite, name='favorite'),
    path('category/', views.show_tag, name='show_tag'),
]