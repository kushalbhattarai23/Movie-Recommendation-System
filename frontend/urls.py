from django.urls import path
from .views import *
from movies.views import *
urlpatterns = [
    path('',HomeView.as_view(), name='home'),
    path('login/', login_view, name='logins'), 
    path('register/', register_view, name='register'),
    path('logout/', logout_view, name='logouts'),
    path('movies/', MovieViewSet.as_view({'get': 'list'}), name='movie-list'), 
    path('movies/<int:movie_id>/', movie_detail, name='movie_details'),
    path('rate_movie/', rate_movie, name='rate_movie'),
]
