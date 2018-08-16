import requests
from .host import host
from . import services
from django.shortcuts import render, redirect
from django.contrib import messages

def getToken(username, password):
    url = host + '/api-token-auth/'
    data= {
        'username': username,
        'password': password
    }
    try:
        response = requests.post(url, json=data)
        return response.json()
    except:
        return {
            'error': 'Failed to get token'
        }

def verifyToken(old):
    url = host + '/api-token-verify/'
    data = {
        'token': old
    }
    try:
        response = requests.post(url, json=data)
        return response.json()
    except:
        return {
            'error': 'Token failed to verify'
        }

def refreshToken(old):
    url = host + '/api-token-refresh/'
    data = {
        'token': old
    }
    try:
        response = requests.post(url, json=data)
        return response.json()
    except:
        return {
            'error': 'Token failed to refresh'
        }

def login_required(function):
    def wrapper(request, *args, **kwargs):
        try:
            token = token = request.COOKIES['token']
            token = verifyToken(token)
            if token['token']:
                response = function(request, *args, **kwargs)
                token = refreshToken(token['token'])
                response.set_cookie(key='token', value=token['token'])
                return response
        except:
            messages.add_message(request, messages.ERROR, 'Session expired. Login again')
            return redirect('application:login')
    return wrapper