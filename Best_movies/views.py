from django.shortcuts import render
from django.shortcuts import render
from django.http import HttpResponse
from Best_movies.models import Movie,Review,FavoriteList,User
from Best_movies.forms import UserForm, UserProfileForm
from django.shortcuts import redirect
from django.urls import reverse
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from datetime import datetime
import datetime
import re
# Create your views here.
def index(request):
    movie_list = Movie.objects.order_by('-date')[:3]
    context_dict = {}
    popular_list = Movie.objects.order_by('-date').order_by('-average_rating')[:4]

    context_dict['movies'] = movie_list
    context_dict['popular'] = popular_list
    response = render(request, 'Best_movies/index.html', context=context_dict)
    #visitor_cookie_handler(request)
    return response
    # return HttpResponse("Rango says hey there partner!(<a href='/rango/about/'>About</a>)")
def register(request):
    registered=False
    if request.method=="POST":
        user_form=UserForm(request.POST)
        profile_form=UserProfileForm(request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            user=user_form.save()
            user.set_password(user.password)
            user.save()
            profile=profile_form.save(commit=False)
            profile.user=user

            if 'picture' in request.FILES:
                profile.picture=request.FILES['picture']
            profile.save()
            registered=True
        else:
            print(user_form.errors, profile_form.errors)
    else:
        user_form=UserForm()
        profile_form=UserProfileForm()
    return render(request,'Best_movies/register.html',context={'user_form': user_form,'profile_form':profile_form,'registered':registered})

def user_login(request):
    if request.method=="POST":
        username=request.POST.get('username')
        password=request.POST.get('password')

        user=authenticate(username=username,password=password)
        if user:
            if user.is_active:
                login(request,user)
                return redirect(reverse('Best_movies:index'))
            else:
                return HttpResponse("Your Rango account is disabled.")
        else:
            print(f"Invalid login details:{username},{password}")
            return HttpResponse("Invalid login details supplied.")
    else:
        return  render(request,'Best_movies/login.html')
def search(request):
    context_dict ={}
    movie_name=[]
    actor_name=[]
    r=request.GET.get("search")
    c = request.GET.get("category")

    if Movie.objects.filter(name__icontains=r):
        movie_name=Movie.objects.filter(name__icontains=r)

    elif Movie.objects.filter(actor__icontains=r):
        actor_name = Movie.objects.filter(actor__icontains=r)
    if c == "All":
        context_dict['movie_name'] = movie_name
        context_dict['actor_name'] = actor_name
    elif c=="title":
        context_dict['movie_name'] = movie_name
    elif c=="actor":
        context_dict['actor_name'] = actor_name

    context_dict['category']=c
    context_dict['result']=r
    print(context_dict)
    return render(request,'Best_movies/search.html', context=context_dict)
def detail(request,name):
    context_dict = {}
    try:
        movie =Movie.objects.get(slug=name)
        review=Review.objects.filter(movie=movie)
        context_dict['movie'] = movie
        context_dict['reviews']=review
    except:
        context_dict['movie'] = None
        context_dict['reviews'] = None
    return render(request, 'Best_movies/movie.html', context=context_dict)

@login_required
def like(request,id,name,username):
    if username!="":
        context_dict = {}
        review=Review.objects.get(id=id)
        review.user_list=review.user_list+username+','
        review.like+=1
        review.save()
        return redirect(reverse('Best_movies:detail', kwargs={'name': name}))
@login_required
def dislike(request,id,name,username):
    if username != "":
        review = Review.objects.get(id=id)
        review.user_list = review.user_list+username+','
        review.dislike += 1
        review.save()
        return redirect(reverse('Best_movies:detail', kwargs={'name': name}))

@login_required
def add_review(request,username,name):
    try:
        user = User.objects.get(username=username)
        movie = Movie.objects.get(slug=name)
    except User.DoesNotExist:
        user=None
    if user is None:
        return redirect('/Best_movies/login.html')
    if request.method=='POST':
        content=request.POST.get('review')
        title = request.POST.get('title')
        rating=request.POST.get('rating')
        r = Review.objects.get_or_create(user=user, title=title,movie=movie,date=datetime.datetime.now())[0]
        r.content=content
        r.rating=rating
        r.save()
        return redirect(reverse('Best_movies:detail',kwargs={'name': name}))


    return render(request,'Best_movies/index.html')

@login_required
def favorite(request,username):
    context_dict={}
    movies=[]
    try:
        user = User.objects.get(username=username)
        favorite=FavoriteList.objects.get(user=user)
        for i in re.findall("\d+", favorite.movie):
            if Movie.objects.get(id=int(i)):
                movie = Movie.objects.get(id=int(i))
                movies.append(movie)
        context_dict["movies"] = movies
    except User.DoesNotExist:
        user=None
    except FavoriteList.DoesNotExist:
        favorite=None
    if user is None:
        return redirect('/Best_movies/login.html')

    return render(request, 'Best_movies/favorite.html', context=context_dict)

def show_tag(request):
    context_dict={}
    movie=Movie.objects.all()
    genre=request.POST.get('mark')
    context_dict['genre']=genre
    category = request.POST.get('mark1')
    context_dict['category'] = category
    Production_country = request.POST.get('mark2')
    context_dict['Production_country'] = Production_country
    date=request.POST.get('mark3')
    context_dict['date'] = date


    for key,value in context_dict.items():
        if value == None or value =='all':
            continue
        else:
            if key=='category':
                movie &=Movie.objects.filter(category=value)
            if key == 'genre':
                movie &= Movie.objects.filter(genre=value)
            if key == 'Production_country':
                movie &= Movie.objects.filter(Production_country=value)
            if key=='date':
                context_dict['date'] = int(date)
                start = datetime.date(context_dict['date'], 1, 1)
                end = datetime.date(context_dict['date'] + 1, 1, 1)
                movie &= Movie.objects.filter(date__range=(start, end))
    context_dict['movies']=movie
    return render(request, 'Best_movies/category.html',context=context_dict)
@login_required
def user_logout(request):
    logout(request)
    return redirect(reverse('Best_movies:index'))

def add_movie(request,id,username):

    context_dict={}
    movies=[]
    user = User.objects.get(username=username)

    favorite=FavoriteList.objects.get_or_create(user=user)[0]

    favorite.movie=favorite.movie+str(id)+","
    favorite.save()
    print(favorite.movie)
    for i in re.findall("\d+", favorite.movie):
        if Movie.objects.get(id=int(i)):
            movie = Movie.objects.get(id=int(i))
            movies.append(movie)
    context_dict["movies"] = movies
    return render(request, 'Best_movies/favorite.html', context=context_dict)
