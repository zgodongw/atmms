import requests
import datetime
from requests_jwt import JWTAuth
from .host import host
from .datamodels import (
    Organisation,Site, Asset,
    Activity, Message, Profile,
    User
)
from . import authentication


def getTime(time):
    try:
        pytime = datetime.datetime.strptime(time, '%Y-%m-%dT%H:%M:%SZ')
    except:
        pytime = datetime.datetime.strptime(time, '%Y-%m-%dT%H:%M:%S.%fZ')
    new = '{:%Hh%Mm%Ss}'.format(pytime)
    return new

def getOrganisations():
    url = host + '/organisation/'
    try:
        response = requests.get(url)
        organisations = response.json()
        allOrgs = []

        for org in organisations:
            orgObj = Organisation(org['id'], org['name'])
            allOrgs.append(orgObj)
        return allOrgs
    except:
        return allOrgs

def getOrgForSites(id):
    url = host + '/organisation/'
    try:
        response = requests.get(url)
        organisations = response.json()
        for org in organisations:
            if org['id'] == id:
                return org['name']
        else:
           return "none" 
    except:
        return "none"

def getOrgID(name):
    url = host + '/organisation/'
    try:
        response = requests.get(url)
        organisations = response.json()
        for org in organisations:
            if org['name'] == name:
                return org['id']
        else:
           return 0
    except:
        return 0
        
def getActivitiesFor(deviceID):
    url = host + '/asset/activity/'
    try:
        params = {'q': deviceID}
        response = requests.get(url, params=params)
        activities = response.json()
        return activities
    except:
        return []

def getAssets(site=None):
    url = host + '/asset/'
    params= {'q': site}
    try:
        response = requests.get(url, params=params)
        assets = response.json()
        allAssets = []
        for name in assets:
            assetObj = Asset(
                name['id'], name['deviceName'],
                name['deviceID'], name['location'],
                name['site']
            )
            allAssets.append(assetObj)
        return allAssets
    except:
        return []

def getSites(orgId):
    url = host + '/site/'
    organisation = getOrgForSites(orgId)
    params = {'q': organisation}
    try:
        response = requests.get(url, params)
        sites = response.json()
        allSites = []
        for place in sites:
            siteObj = Site(place['place'], place['id'], place['province'])
            allSites.append(siteObj)
        return allSites
    except:
        return []

def getProfile(token):
    url = host + '/account/user/'
    try:
        headers = {
            'Authorization': 'JWT ' + token
        }
        response = requests.get(url, headers=headers)
        users = response.json()
        userInfo = []
        for user in users:
            usersObj = Profile(
                user['id'], user['username'], user['profile']['organisation'],
                user['profile']['defaultSite'], user['profile']['color']
            )
            userInfo.append(usersObj)
        return userInfo
    except:
        return []

def getUserIDFor(token):
    url = host + '/account/user-only/'
    try:
        headers = {
            'Authorization': 'JWT ' + token
        }
        response = requests.get(url, headers=headers)
        users = response.json()
        userInfo = []
        for user in users:
            usersObj = User(
                user['id'], user['username'],
            )
            userInfo.append(usersObj)
        return userInfo
    except:
        return []

def getLineData(key, activities):
    allActivities = []
    for attribute in activities:
        if key == 'datetime':
            allActivities.append(getTime(attribute[key]))
        else:
            allActivities.append(attribute[key])
    return allActivities[-10:]

def getMessages():
    url = host + '/message/'
    try:
        response = requests.get(url)
        messages = response.json()
        allMessages = []
        for message in messages:
            messageObj = Message(message['message'], message['username'], getTime(message['timestamp']))
            allMessages.append(messageObj)
        return allMessages[-20:]
    except:
        return []

def sendMessage(message, username, timestamp):
    url = host + '/message/add/'
    data={
        'message':message,
        'username': username,
        'timestamp': timestamp
    }
    try:
        response = requests.post(url, json=data)
        return response
    except:
        return {
            'error': 'Message failed to send'
        }
        
def manipulateAsset(sites, deviceID, deviceName, place, location, update=False):
    if update:
        url = host + '/asset/'+ deviceID +'/update/'
    else:
        url = host + '/asset/add/'

    siteid = int()
    for site in sites:
        if site.place == place:
            siteid = site.id
    if siteid:
        data = {
            'deviceID': deviceID,
            'deviceName': deviceName,
            'site': siteid,
            'location': location
        }
        if update:
            try:
                response = requests.put(url, json=data)
                response.json()
                return response
            except:
                return {
                    'error': 'Sorry, couldn\'t connect,\
                    please check your internet connection'
                }
        else:
            try:
                response = requests.post(url, json=data)
                response.json()
                return response
            except:
                return {
                    'error': 'Sorry, couldn\'t connect,\
                    please check your internet connection'
                }
    else:
        return {
            'error':'No such site exists'
        }

def registerUser(
        username, password,
        organisation, province,
        email
    ):
    url = host + '/account/register/'
    url2 = host + '/account/profile/create/'

    # First register a user
    dataR = {
        'username' : username,
        'email': email ,
        'password': password,
        'first_name': '',
        'last_name': ''
    }

    try:
        response = requests.post(url, json=dataR)

        orgID = getOrgID(organisation)

        # Then create a default profile
        token = authentication.getToken(username, password)

        user = getUserIDFor(token['token'])

        userID = user[0].id
        dataP = {
            'user': userID,
            'organisation': orgID,
            'defaultSite': province,
            'color': '30a5ff'
        }
        headers = {
                'Authorization': 'JWT ' + token['token']
        }
        response = requests.post(url2, json=dataP, headers=headers)
        return True
    except:
        return False