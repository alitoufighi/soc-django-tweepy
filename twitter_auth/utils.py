#!/usr/bin/python
# -*- coding: utf-8 -*-
import tweepy
import requests
from InstagramAPI import InstagramAPI
import sys
import importlib
importlib.reload(sys)
#
# reload(sys)
sys.setdefaultencoding('utf8')
CONSUMER_KEY = 'YkbgnKkRGXuXaIO7QxM5QcHVB'
CONSUMER_SECRET = 'XOYVldvUOnkSkrtFRUh6ixV4HANKfYKlYLIDnstSTreg7mOLQJ'

TELE_TOKEN = '332670886:AAENLmE6sF8sx5RKeXqfF16X2nJFylvd9EY'

INSTA_API_KEY = ''
ONSTA_API_SECRET = ''

def telegram_send_message(file_host_address, text, id, file_address=None): # file type?
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
	else:
		# response = requests.post(
		# 	url='https://api.telegram.org/bot{0}/{1}'.format(TELE_TOKEN, 'sendPhoto'),
		# 	data={'chat_id': '@imatovimatovimatovimatovimatov'},
		# 	files={'photo': open(file_address, 'rb'), }).json()
		# file_id = response['result']['photo'][1]['file_id']
		# response = requests.get(
		# 	url='https://api.telegram.org/bot{0}/getFile?file_id={1}'.format(TELE_TOKEN, file_id),
		# ).json()
		# file_path = response['result']['file_path']
		# file_url='https://api.telegram.org/file/bot{0}/{1}'.format(TELE_TOKEN, file_path)
		# print (file_address)
		# host=request.get_host()
		# print (host)
		# file_address=host+file_address
		print (file_host_address)
		text='[​​​​​​​​​​​]({0}) {1}'.format(file_host_address,text)
		method = 'sendMessage'
		# print (text)
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

# def get_insta_api(request):

def instagram_send_message(request, text, file):
	insta_un = request.session.get('insta_id')
	insta_pw = request.session.get('insta_pw')
	Insta = InstagramAPI(insta_un, insta_pw)
	Insta.login()  # login
	Insta.uploadPhoto(file, caption=text)