from argparse import Action
from turtle import title
from unittest import result
from django.contrib import messages
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from .models import User, Movie, Favorite_Movie, watch_list, Comment, Activity
import datetime
from django.views.generic.edit import CreateView
from .forms import UserAccount
from django.db.models import Q
import os

moviesData = Movie.objects.all().order_by('-uploaded_on')

class createAccount(CreateView):
    form_class = UserAccount
    success_url = reverse_lazy('login')
    template_name = 'signup.html'
    
def index(request):
    fav_count = Favorite_Movie.objects.all(movie = moviesData.id)
    return render(request, 'home.html', {'movies': moviesData, 
                                         'Liked_by': fav_count})

def movies(request): 
    return render(request, "movies.html", {'movies': moviesData})

def movie(request, mpk):
    movie = Movie.objects.get(id = mpk)
    mComments = Comment.objects.all()
    comCount = Comment.objects.filter(id = mpk).count()
    return render(request, 'movie.html', {'movie': movie, 
                                          'comments': mComments, 
                                          'commentNum': comCount})

def movieInfo(request, mpk, uid):
    movie = Movie.objects.get(id = mpk)
    mComments = Comment.objects.all()
    comCount = Comment.objects.filter(id = mpk).count()
    watch = watch_list.objects.filter(user = uid)
    favs = Favorite_Movie.objects.all()
    return render(request, 'movie.html', {'movie': movie, 
                                          'comments': mComments, 
                                          'commentNum': comCount, 
                                          'watchlist': watch, 
                                          'favs': favs})


def uploadMovie(request):
    if request.method == 'POST':
        if len(request.FILES) != 0:
            mTitle = request.POST['title']
            aNames = request.POST['actors']
            rDate = request.POST['release_date']
            mGenre = request.POST['genre']
            mType = request.POST['type']
            mPoster = request.FILES['poster']
            trailerLink = request.POST['link']
            username = request.POST['user']
            publisher = User(request.POST['uploaded_by'])
            published_on = datetime.datetime.now()
            uploaded_movie = request.FILES['movie']
            mDesc = request.POST['description']
            newMovie = Movie(title = mTitle, release_date = rDate, main_actors = aNames, genre = mGenre, movie_type = mType, description = mDesc, poster = mPoster, trailer_link = trailerLink, uploaded_by = publisher, uploaded_on = published_on, movie = uploaded_movie)
            newMovie.save()
            newActivity = Activity(user = publisher, action = f'Published {newMovie.movie}', time = published_on)
            newActivity.save()
            myAcc = User.objects.get(username = username)
            return redirect('myMovies', myAcc.id)
    return render(request, 'upload.html')

def myMovies(request, uid):
    uploaded_movies = Movie.objects.filter(uploaded_by = uid).order_by('-uploaded_on')
    return render(request, 'mymovies.html', {'upMovies': uploaded_movies})

def myfavs(request, uid):
    uploaded_movies = Favorite_Movie.objects.filter(user = uid)
    return render(request, 'myfavs.html', {'upMovies': uploaded_movies})

def watchlist(request, uid):
    uploaded_movies = watch_list.objects.filter(user = uid)
    return render(request, 'watchlist.html', {'upMovies': uploaded_movies})

def editMovie(request, mid):
    updateMovie = Movie.objects.get(id = mid)
    if request.method == "POST":
        updateMovie.title = request.POST['title']
        updateMovie.main_actors = request.POST['actors']
        updateMovie.genre = request.POST['genre']
        updateMovie.release_date= request.POST['rDate']
        updateMovie.trailer_link = request.POST['link']
        updateMovie.description = request.POST['desc']
        updateMovie.save()
        
        newActivity = Activity(user = updateMovie.uploaded_by, action = f'Edited {Movie(updateMovie.title)}', time = datetime.datetime.now())
        newActivity.save()
        user = User.objects.get(username = updateMovie.uploaded_by)
        return redirect('myMovies', user.id)
    return render(request, 'updateMovie.html', {'movie': updateMovie})

def deleteMovie(request, mid):
    movieInfo = Movie.objects.get(id = mid)
    usrInfo = User.objects.get(username = movieInfo.uploaded_by)
    movieInfo.delete()
    return redirect('myMovies', usrInfo.id)

def kids(request):
    kidsMovies = Movie.objects.filter(movie_type = "K")
    return render(request, "kids.html", {'movies': kidsMovies})

def adults(request):
    adMovies = Movie.objects.filter(movie_type = "A")
    return render(request, "adults.html", {'movies': adMovies})
    
def profile(request, pk):
    userInfo = User.objects.get(id=pk)
    actions = Activity.objects.filter(user = pk).order_by('-time')
    if request.method == "POST":
        
        if len(request.FILES) != 0:
            if len(userInfo.profile_image) > 0:
                os.remove(userInfo.profile_image.path)
            userInfo.profile_iamge = request.FILES['profile_pic']
        
        userInfo.first_name = request.POST['fname']
        userInfo.last_name  = request.POST['lname']
        userInfo.email  = request.POST['email']
        userInfo.username  = request.POST['username']
        userInfo.age  = request.POST['age']
        
        if request.POST['gender'] == "Male" or request.POST['gender'] == "male" or request.POST['gender'] == "M" or request.POST['gender'] == "m" or request.POST['gender'] == "MALE":
            userInfo.gender  = "M"
        elif request.POST['gender'] == "Female" or request.POST['gender'] == "female" or request.POST['gender'] == "F" or request.POST['gender'] == "f" or request.POST['gender'] == "FEMALE":
            userInfo.gender  = "F"
        else:
            userInfo.gender  = "O"
            
        userProf = User(request.POST['user'])        
        userInfo.save()
        newActivity = Activity(user = userProf, action = 'Updated your account Info', time = datetime.datetime.now())
        newActivity.save()
        messages.success(request, 'User account updated successfully!')
        return redirect('profile', userInfo.id)
        
    context = {'user': userInfo, 'activities': actions}
    return render(request, 'profile.html', context)

def addToFavorites(request, mpk, upk):
    favUser = User.objects.get(id = upk)
    favMovie = Movie.objects.get(id = mpk)
    newfav = Favorite_Movie(user = favUser, movie = favMovie)
    newfav.save()
    return redirect('movieInfo', mpk, upk)

def addTowatchList(request, mpk, upk):
    watchUser = User.objects.get(id = upk)
    watchMovie = Movie.objects.get(id = mpk)
    newWlist = watch_list(user = watchUser, movie = watchMovie)
    newWlist.save()
    return redirect('movieInfo', mpk, upk)

def search(request):
    if request.method == 'POST':
        keyword = request.POST['search']
        response = Movie.objects.filter(title__icontains = keyword)
        resCounter = Movie.objects.filter(title__icontains = keyword).count()
        return render(request, 'results.html', {'key': keyword, 
                                                'results': response,
                                                'resCount': resCounter})
    else:
        return render(request, 'results.html', {'res': 'Not found'})
    
def adSearch(request, uid):
    if request.method == 'POST':
        keyword = request.POST['search']
        response = Movie.objects.filter(title__icontains = keyword)
        resCounter = Movie.objects.filter(title__icontains = keyword).count()
        return render(request, 'results.html', {'key': keyword, 
                                                'results': response,
                                                'resCount': resCounter})
    else:
        return render(request, 'results.html', {'res': 'Not found'})
    
def kidSearch(request, uid):
    if request.method == 'POST':
        keyword = request.POST['search']
        response = Movie.objects.filter(title__icontains = keyword)
        resCounter = Movie.objects.filter(title__icontains = keyword).count()
        return render(request, 'results.html', {'key': keyword, 
                                                'results': response,
                                                'resCount': resCounter})
    else:
        return render(request, 'results.html', {'res': 'Not found'})


def filter(request):
    if request.method == 'POST':
        keyword = request.POST['filter']
        value = request.POST['value']
        
        if request.POST['filter'] == "genre":
            response = Movie.objects.filter(genre__icontains = value)
            resCounter = Movie.objects.filter(genre__icontains = value).count()
            return render(request, 'filter-results.html', {'key': keyword, 
                                                           'val': value,
                                                            'mResults': response,
                                                            'movies': moviesData,
                                                            'resCount': resCounter})
        elif request.POST['filter'] == "release_date":
            response = Movie.objects.filter(release_date__icontains = value)
            resCounter = Movie.objects.filter(release_date__icontains = value).count()
            return render(request, 'filter-results.html', {'key': keyword, 
                                                           'val': value,
                                                            'mResults': response,
                                                            'movies': moviesData,
                                                            'resCount': resCounter})
            
        else:
            response = Movie.objects.filter(main_actors__icontains = value)
            resCounter = Movie.objects.filter(main_actors__icontains = value).count()
            return render(request, 'filter-results.html', {'key': keyword, 
                                                           'val': value,
                                                            'mResults': response,
                                                            'movies': moviesData,
                                                            'resCount': resCounter}) 
    else:
        return render(request, 'filter-results.html', {'res': 'Not found'})    

def adFilter(request):
    if request.method == 'POST':
        keyword = request.POST['filter']
        value = request.POST['value']
        
        if request.POST['filter'] == "genre":
            response = Movie.objects.filter(movie_type = "A", genre__icontains = value)
            resCounter = Movie.objects.filter(movie_type = "A", genre__icontains = value).count()
            return render(request, 'ad-filter.html', {'key': keyword, 
                                                           'val': value,
                                                            'mResults': response,
                                                            'movies': moviesData,
                                                            'resCount': resCounter})
        elif request.POST['filter'] == "release_date":
            response = Movie.objects.filter(movie_type = "A", release_date__icontains = value)
            resCounter = Movie.objects.filter(movie_type = "A", release_date__icontains = value).count()
            return render(request, 'ad-filter.html', {'key': keyword, 
                                                           'val': value,
                                                            'mResults': response,
                                                            'movies': moviesData,
                                                            'resCount': resCounter})
            
        else:
            response = Movie.objects.filter(movie_type = "A", main_actors__icontains = value)
            resCounter = Movie.objects.filter(movie_type = "A", main_actors__icontains = value).count()
            return render(request, 'ad-filter.html', {'key': keyword, 
                                                           'val': value,
                                                            'mResults': response,
                                                            'movies': moviesData,
                                                            'resCount': resCounter}) 
    else:
        return render(request, 'ad-filter.html', {'res': 'Not found'})
    
def kidsFilter(request):
    if request.method == 'POST':
        keyword = request.POST['filter']
        value = request.POST['value']
        
        if request.POST['filter'] == "genre":
            response = Movie.objects.filter(movie_type = "K", genre__icontains = value)
            resCounter = Movie.objects.filter(movie_type = "K", genre__icontains = value).count()
            return render(request, 'ad-filter.html', {'key': keyword, 
                                                           'val': value,
                                                            'mResults': response,
                                                            'movies': moviesData,
                                                            'resCount': resCounter})
        elif request.POST['filter'] == "release_date":
            response = Movie.objects.filter(movie_type = "K", release_date__icontains = value)
            resCounter = Movie.objects.filter(movie_type = "K", release_date__icontains = value).count()
            return render(request, 'ad-filter.html', {'key': keyword, 
                                                           'val': value,
                                                            'mResults': response,
                                                            'movies': moviesData,
                                                            'resCount': resCounter})
            
        else:
            response = Movie.objects.filter(movie_type = "K", main_actors__icontains = value)
            resCounter = Movie.objects.filter(movie_type = "K", main_actors__icontains = value).count()
            return render(request, 'ad-filter.html', {'key': keyword, 
                                                           'val': value,
                                                            'mResults': response,
                                                            'movies': moviesData,
                                                            'resCount': resCounter}) 
    else:
        return render(request, 'ad-filter.html', {'res': 'Not found'})
    
def help(request):
    return render(request, 'help-center.html')