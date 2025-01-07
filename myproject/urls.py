"""
URL configuration for My_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from accounts import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('login/', views.user_login, name='login'),
    path('signup/', views.signup, name='signup'),
    path('logout/', views.logout, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('settings/', views.settings_view, name='settings'),
    path('profile/', views.profile, name='profile'),
    path('helpcenter/', views.helpcenter, name='helpcenter'),
    path('subscription/', views.subscription, name='subscriptions'),
    path('spotify/login/', views.spotify_login, name='spotify_login'),
    path('callback/', views.spotify_callback, name='spotify_callback'),
    path('categories/', views.categories, name='categories'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('signout/', views.signout, name='signout'),
    path('spotifyprofile/', views.spotifyprofile, name='spotifyprofile'),
    path('voice_search/', views.voice_search, name='voice_search'),
    path('process_voice/', views.process_voice, name='process_voice'),
    path('songs/', views.songs_view, name='songs'),
    path('podcasts/', views.podcasts_view, name='podcasts'),
    path('genres/', views.genres_view, name='genres'),
    path('artists/', views.artists_view, name='artists'),
    path('playlists/', views.playlists_view, name='playlists')
    ]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
