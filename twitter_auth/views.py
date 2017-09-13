# Create your views here.
import tweepy
# import requests

from time import sleep
from django.http import *
from django.shortcuts import render_to_response, render
from django.core.urlresolvers import reverse
from django.contrib.auth import logout
from django.utils import timezone
from django.conf import settings
import os
from mimetypes import guess_type


from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import logging


from .forms import *
from .models import *

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
        api = get_twitter_api(request)
        request.session.clear()
        logout(request)
    return HttpResponseRedirect(reverse('main'))


def info(request):
    if check_key(request):

        if 'telegram' in request.POST:
            request.session['telegram_id'] = request.POST['telegram-id']

        telegram_id = request.session.get('telegram_id', None)
            if not telegram_id:
                request.session['telegram_id'] = None

        try:
            twitter_api = get_twitter_api(request)
            user = twitter_api.me()
        except tweepy.TweepError:
            return render(request, 'twitter_auth/vpn.html')

        if 'post' in request.POST:
            form = PostForm(request.POST, request.FILES)
            if form.is_valid():
                post = form.save(commit=False)
                post.published_date = timezone.now()
                post.save()

                # x = guess_type('127.0.0.1:8000/info/', strict=True)
                # print (x)

                if post.media: # Post with media
                    file_address = "%s%s" % (settings.MEDIA_ROOT, post.media)
                    twitter_api.update_with_media(filename=file_address, status=post.text)
                    telegram_send_message(text=post.text, id=request.session['telegram_id'], file_address=file_address)
                    os.remove(file_address)
                else: # Post only with text
                    if request.session['telegram_id']:
                        print('Sent To Telegram!')
                        telegram_send_message(text=post.text, id=request.session['telegram_id'])



            else:
                print ('invalid form')
                post = Post(text='')
        else:
            form = PostForm()
            post = Post(text='')
        return render(request, 'twitter_auth/info.html', {'user': user, 'post': post, 'form': form, 'teleid': request.session['telegram_id']})
    else:
        return HttpResponseRedirect(reverse('main'))


def auth(request):
    oauth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET, '/callback/')
    sleep(0.1) # To prevent continuous requests to twitter
    auth_url = oauth.get_authorization_url(True)
    response = HttpResponseRedirect(auth_url)
    # store the request token in user session
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
