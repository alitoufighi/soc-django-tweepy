# Create your views here.
import tweepy
# import requests
from time import sleep
from django.http import *
from django.shortcuts import render_to_response, render, get_object_or_404
from django.core.urlresolvers import reverse
from django.contrib.auth import logout
from django.utils import timezone
# from .settings import MEDIA_ROOT
from django.conf import settings
import requests


from .forms import PostForm
from .models import Post

# from twitter_auth.utils import *

from twitter_auth.utils import *


def main(request):
    """
    main view of app, either login page or info page
    """
    # if we haven't authorised yet, direct to login page
    if check_key(request):
        return HttpResponseRedirect(reverse('info'))
    else:
        return render_to_response('twitter_auth/login.html')


def unauth(request):
    """
	logout and remove all session data
	"""
    if check_key(request):
        api = get_api(request)
        request.session.clear()
        logout(request)
    return HttpResponseRedirect(reverse('main'))


def info(request):
    # print(check_key)
    if check_key(request):
        api = get_api(request)
        user = api.me()
        if request.method == 'POST':
            form = PostForm(request.POST, request.FILES)
            if form.is_valid():
                post = form.save(commit=False)
                post.published_date = timezone.now()
                post.save()

                file_address = "%s%s" % (settings.MEDIA_ROOT, post.media)
                # api.update_status(status=post.text)
                api.update_with_media(filename=file_address, status=post.text)
                
                # return render_to_response('twitter_auth/info.html', {'user': user, 'post': post})
            else:
                print ('invalid form')
                post = Post(text='')
        else:
            form = PostForm()
            post = Post(text='')
        # return render_to_response('twitter_auth/info.html', {'user': user, 'post': post, 'form': form})
        return render(request, 'twitter_auth/info.html', {'user': user, 'post': post, 'form': form})
    else:
        return HttpResponseRedirect(reverse('main'))


def auth(request):
    # consumer_key = 'YkbgnKkRGXuXaIO7QxM5QcHVB'
    # consumer_secret = 'XOYVldvUOnkSkrtFRUh6ixV4HANKfYKlYLIDnstSTreg7mOLQJ'
    oauth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET, 'http://alitou.pythonanywhere.com/callback/')
    sleep(1)
    auth_url = oauth.get_authorization_url(True)
    # print (auth_url)
    # print (oauth.access_token)
    # auth_url = oauth.get_authorization_url(True)
    response = HttpResponseRedirect(auth_url)
    # store the request token
    request.session['request_token'] = oauth.request_token
    return response


def callback(request):
    verifier = request.GET.get('oauth_verifier')
    oauth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    token = request.session.get('request_token')
    request.session.delete('request_token')
    oauth.request_token = token
    try:
        oauth.get_access_token(verifier)
    except tweepy.TweepError:
        print('Error, failed to get access token')

    request.session['access_key_tw'] = oauth.access_token
    request.session['access_secret_tw'] = oauth.access_token_secret
    print(request.session['access_key_tw'])
    print(request.session['access_secret_tw'])
    response = HttpResponseRedirect(reverse('info'))
    return response


def check_key(request):
    """
	Check to see if we already have an access_key stored, if we do then we have already gone through
	OAuth. If not then we haven't and we probably need to.
	"""
    try:
        access_key = request.session.get('access_key_tw', None)
        if not access_key:
            return False
    except KeyError:
        return False
    return True
