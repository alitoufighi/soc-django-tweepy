# Create your views here.
import tweepy
from InstagramAPI import InstagramAPI

# import requests

from time import sleep
from django.http import *
from django.shortcuts import render_to_response, render
from django.core.urlresolvers import reverse
from django.contrib.auth import logout
from django.utils import timezone
from django.conf import settings
from django.core.files.storage import FileSystemStorage
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
    # if check_twitter_key(request):
    return HttpResponseRedirect(reverse('info'))
    # else:
    #     return render_to_response('twitter_auth/login.html')


def unauth(request):
    """
	logout and remove all session data
	"""
    if check_twitter_key(request):
        api = get_twitter_api(request)
        request.session.clear()
        logout(request)
    return HttpResponseRedirect(reverse('main'))


def info(request):
    if 'telegram' in request.POST:
        request.session['telegram_id'] = request.POST['telegram-id']

    telegram_id = request.session.get('telegram_id', None)

    if 'insta' in request.POST:
        request.session['insta_id'] = request.POST['insta-un']
        request.session['insta_pw'] = request.POST['insta-pw']
    insta_id = request.session.get('insta_id', None)

    if 'insta-remove' in request.POST:
        request.session['insta_id'] = None

    if 'tele-remove' in request.POST:
        request.session['telegram_id'] = None

    # try:
    #     twitter_api = get_twitter_api(request)
    #     # user = twitter_api.me()
    # except tweepy.TweepError:
    #     return render(request, 'twitter_auth/vpn.html')

    if 'post' in request.POST:
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.published_date = timezone.now()
            post.save()

            if post.media: # Post with media
                file_address = "%s/%s" % (settings.MEDIA_ROOT, post.media)
                fs = FileSystemStorage()
                filename = fs.save(post.media.name, post.media)
                uploaded_file_url = fs.url(filename)
                host = request.get_host()
                uploaded_file_url=host + uploaded_file_url
                print ('host:', host)
                print ('file address', file_address)
                print ('url:', uploaded_file_url)
                if telegram_id != None:
                    telegram_send_message(uploaded_file_url, text=post.text, id=request.session['telegram_id'], file_address=file_address)

                if insta_id != None:
                    instagram_send_message(request, text= post.text, file=file_address)

                if 'twitter' in request.session != None:
                    pass
                    # twitter_api.update_with_media(filename=file_address, status=post.text)

                # os.remove(file_address)
            else: # Post only with text
                if 'telegram_id' in request.session != None:
                    telegram_send_message(text=post.text, id=request.session['telegram_id'])
                if 'twitter' in request.session:
                    pass
                    # twitter_api.update_status(status=post.text)






        else:
            print ('invalid form')
            post = Post(text='')
    else:
        form = PostForm()
        post = Post(text='')
    # return render(request, 'twitter_auth/info.html', {'user': user, 'post': post, 'form': form, 'teleid': request.session['telegram_id']})
    return render(request, 'twitter_auth/info.html',
                      {'post': post, 'form': form, 'teleid': request.session['telegram_id'], 'instaid': request.session['insta_id']})
    # else:
    #     return HttpResponseRedirect(reverse('main'))


def auth(request):
    oauth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET, 'http://alitou.pythonanywhere.com/callback/')
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
    response = HttpResponseRedirect(reverse('info'))
    return response


def check_twitter_key(request):
    try:
        # access_key = request.session.get('access_key_tw', None)
        access_key = request.session.get('')
        if not access_key:
            return False
    except KeyError:
        return False
    return True

# def check_telegram_id(request):
#         id = request.session.get('telegram_id')