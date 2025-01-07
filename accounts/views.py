from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.conf import settings
from django.core.mail import send_mail
import logging
import spotipy
from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth
import time
from django.http import JsonResponse
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import requests

# Logger setup
logger = logging.getLogger(__name__)

# Home view
def home(request):
    return render(request, 'home.html')

# User login view
def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        pass1 = request.POST.get('pass1')

        logger.debug(f"Login attempt with username: {username} and password: {pass1}")

        user = authenticate(username=username, password=pass1)

        if user is not None:
            login(request, user)
            next_url = request.GET.get('next', 'dashboard')  # Redirect to next URL or dashboard
            logger.debug(f"Login successful for username: {username}")
            return redirect(next_url)
        else:
            logger.debug(f"Authentication failed for username: {username}")
            messages.error(request, "Invalid username or password.")
            return redirect('login')
    return render(request, "login.html")
    

# Signup view
def signup(request):
    if request.method == "POST":
        username = request.POST.get('username')
        fname = request.POST.get('fname')
        lname = request.POST.get('lname')
        email = request.POST.get('email')
        pass1 = request.POST.get('pass1')
        pass2 = request.POST.get('pass2')

        # Check if username already exists
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists! Please try another username.")
            return redirect('signup')
        
        # Check if email already exists
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email is already registered.")
            return redirect('signup')
        
        # Check username length
        if len(username) > 15:
            messages.error(request, "Username must be under 15 characters.")
            return redirect('signup')

        # Check if passwords match
        if pass1 != pass2:
            messages.error(request, "Passwords do not match.")
            return redirect('signup')

        # Check if username is alphanumeric
        if not username.isalnum():
            messages.error(request, "Username must be alphanumeric!")
            return redirect('signup')
    
        # Create new user
        myuser = User.objects.create_user(username, email, pass1)
        myuser.first_name = fname
        myuser.last_name = lname
        myuser.save()

        # Send welcome email
        messages.success(request, "Your account has been created successfully.")
        subject = "Welcome to Emusic Family"
        message = f"Hello {myuser.first_name}!!\nWelcome to Emusic Application!!\nThank you for registering."
        from_email = settings.EMAIL_HOST_USER
        to_list = [myuser.email]
        send_mail(subject, message, from_email, to_list, fail_silently=True)

        return redirect('login')

    return render(request, "signup.html")

# Signout view
def signout(request):
    logout(request)
    messages.success(request, "Logged out successfully.")
    return redirect('home')

# Categories view
def categories(request):
    return render(request, 'categories.html')

# Dashboard view
def dashboard(request):
    return render(request, "dashboard.html")

# Settings view
def settings_view(request):
    return render(request, "settings.html")

# Profile view
def profile(request):
    return render(request, "profile.html")

# Help Center view
def helpcenter(request):
    return render(request, "helpcenter.html")

# Subscription view
def subscription(request):
    return render(request, "subscription.html")

# About view
def about(request):
    return render(request, 'about.html')

# Voice Search view
def voice_search(request):
    return render(request, 'voice_search.html')

@csrf_exempt
def process_voice(request):
    if request.method == "POST":
        voice_text = request.POST.get("voice_text", "")
        if voice_text:
            # Redirect to Spotify search with the voice text
            spotify_url = f"https://open.spotify.com/search/{voice_text}"
            return JsonResponse({"message": f"Redirecting to Spotify: {spotify_url}", "url": spotify_url})
        else:
            return JsonResponse({"message": "No voice input received."})
    return JsonResponse({"message": "Invalid request method."})
# Contact view
def contact(request):
    return render(request, 'contact.html')

def spotifyprofile(request):
    return render(request, 'spotifyprofile.html')

def songs_view(request):
    return render(request, 'songs.html')

def podcasts_view(request):
    return render(request, 'podcasts.html')

def genres_view(request):
    return render(request, 'genres.html')

def artists_view(request):
    return render(request, 'artists.html')

def playlists_view(request):
    return render(request, 'playlists.html')

# Spotify login
def spotify_login(request):
    sp_oauth = SpotifyOAuth(
        client_id=settings.SPOTIFY_CLIENT_ID,
        client_secret=settings.SPOTIFY_CLIENT_SECRET,
        redirect_uri=settings.SPOTIFY_REDIRECT_URI,
        scope="user-read-private user-read-email"
    )
    auth_url = sp_oauth.get_authorize_url()
    return redirect(auth_url)

SPOTIFY_AUTH_URL = "https://accounts.spotify.com/authorize"
SPOTIFY_TOKEN_URL = "https://accounts.spotify.com/api/token"
SPOTIFY_API_BASE_URL = "https://api.spotify.com/v1"


# Spotify callback
def spotify_callback(request):
    # Retrieve the authorization code from the callback
    code = request.GET.get('code')
    
    # Exchange the code for an access token
    sp_oauth = SpotifyOAuth(
        client_id=settings.SPOTIFY_CLIENT_ID,
        client_secret=settings.SPOTIFY_CLIENT_SECRET,
        redirect_uri=settings.SPOTIFY_REDIRECT_URI
    )
    try:
        token_info = sp_oauth.get_access_token(code)
        # Save token info in the session for later use
        request.session['token_info'] = token_info
        return render(request,'musichome.html')  # Redirect to a home/dashboard page after success
    except Exception as e:
        return render(request, 'error.html', {'message': f'Error during authentication: {str(e)}'})

def user_top_tracks(request):
    token_info = request.session.get('token_info')
    if not token_info:
        return redirect('spotify-login')
    
    sp = spotipy.Spotify(auth=token_info['access_token'])
    top_tracks = sp.current_user_top_tracks(limit=10)
    
    return render(request, 'top_tracks.html', {'tracks': top_tracks['items']})


