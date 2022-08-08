from turtle import home
from urllib import request
from relecloud import views
from django.contrib import admin
from django.urls import path, include
from django.views.generic.base import TemplateView
from django.conf import settings
from django.conf.urls.static import static
from relecloud.models import Movie, User

movies = Movie.objects.all().order_by('-uploaded_on')[:6]
    
urlpatterns = [
    
    path('admin/', admin.site.urls),
    path('', TemplateView.as_view(template_name='home.html'), {'movies': movies}, name='home'),
    path('home.html', TemplateView.as_view(template_name='home.html'), {'movies': movies}, name='home'),
    path('home', TemplateView.as_view(template_name='home.html'), {'movies': movies}, name='home'),
    path('movies', views.movies, name='movies'),
    path('movie/<str:mpk>', views.movie, name = 'movie'),
    path('movieInfo/<str:mpk>&<str:uid>', views.movieInfo, name = 'movieInfo'),
    path('upload', views.uploadMovie, name='upload'),
    path('adults', views.adults, name='adults'),
    path('kids', views.kids, name='kids'),
    path('relecloud/', include(('relecloud.urls', 'relecloud'))),  
    path('relecloud/', include('django.contrib.auth.urls')),       
    path('profile/<str:pk>', views.profile, name='profile'),
    path('addToFavorites/<str:mpk>&<str:upk>', views.addToFavorites, name = 'addToFavorites'),
    path('addTowatchList/<str:mpk>&<str:upk>', views.addTowatchList, name = 'addTowatchList'),
    path('myMovies/<str:uid>', views.myMovies, name="myMovies"),
    path('watchlist/<str:uid>', views.watchlist, name="watchlist"),
    path('myfavs/<str:uid>', views.myfavs, name="myfavs"),
    path('editMovie/<str:mid>', views.editMovie, name='editMovie'), 
    path('deleteMovie/<str:mid>', views.deleteMovie, name="deleteMovie"),
    path('search', views.search, name='search'),
    path('adSearch/<str:uid>', views.adSearch, name='adSearch'),
    path('kidSearch/<str:uid>', views.kidSearch, name='kidSearch'),
    path('filter', views.filter, name='filter'),
    path('adFilter', views.adFilter, name='adFilter'),
    path('kidsFilter', views.kidsFilter, name='kidsFilter'),
    path('help', views.help, name = 'help'),
    
]+ static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)