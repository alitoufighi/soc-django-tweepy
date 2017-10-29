#!/usr/bin/python
# -*- coding: utf-8 -*-
import tweepy
import requests
from InstagramAPI import InstagramAPI

CONSUMER_KEY = 'YkbgnKkRGXuXaIO7QxM5QcHVB'
CONSUMER_SECRET = 'XOYVldvUOnkSkrtFRUh6ixV4HANKfYKlYLIDnstSTreg7mOLQJ'

TELE_TOKEN = '332670886:AAENLmE6sF8sx5RKeXqfF16X2nJFylvd9EY'

INSTA_API_KEY = ''
ONSTA_API_SECRET = ''

def telegram_send_message(text, id, file_address=None, file_url=None): # file type?
	if file_address == None:
		method = 'sendMessage'
		response = requests.post(
			url='https://api.telegram.org/bot{0}/{1}'.format(TELE_TOKEN, method),
			data={'chat_id': '@{0}'.format(id), 'text': text}).json()
	elif len(text)<=200:
		method = 'sendPhoto'
		response = requests.post(
			url='https://api.telegram.org/bot{0}/{1}'.format(TELE_TOKEN, method),
			data={'chat_id': '@{0}'.format(id), 'caption': text},
			files={'photo': open(file_address, 'rb'),}).json()
			# files={'photo': file_address}).json()
	else:
		text='[​​​​​​​​​​​]({0}){1}'.format(file_url,text)
		method = 'sendMessage'
		response = requests.post(
			url='https://api.telegram.org/bot{0}/{1}'.format(TELE_TOKEN, method),
			data={'chat_id': '@{0}'.format(id), 'text': text, 'parse_mode':'markdown'}).json()
	return response

def get_twitter_api(request):
	oauth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
	access_key = request.session['access_key_tw']
	access_secret = request.session['access_secret_tw']
	oauth.set_access_token(access_key, access_secret)
	api = tweepy.API(oauth)
	return api

def instagram_send_message(request, text, file):
	insta_un = request.session.get('insta_id')
	insta_pw = request.session.get('insta_pw')
	Insta = InstagramAPI(insta_un, insta_pw)
	Insta.login()  # login
	Insta.uploadPhoto(file, caption=text)