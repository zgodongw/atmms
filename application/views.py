from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from . import services
from . import authentication
from datetime import datetime
from django.contrib import messages

# Create your views here.
# I'm not going to use class based views
# because theres a lot of non generic
# functionality I want to implement

@authentication.login_required
def homeView(request):
    profile = services.getProfile(request.COOKIES['token'])
    org = profile[0].organisation
    site = services.getSites(org)
    message = list(reversed(services.getMessages()))
    template = 'home.html'
    context = {'site': site, 'message': message, 'profile': profile}
    return render(request, template, context=context)

@authentication.login_required
def listView(request, place):
    # all the devices that belong to a site
    profile = services.getProfile(request.COOKIES['token'])
    org = profile[0].organisation
    site = services.getSites(org)
    asset = services.getAssets(site=place)
    template = 'listview.html'
    context = {'asset': asset, 'place':place, 'site': site, 'profile': profile}
    return render(request, template, context=context)

@authentication.login_required
def detailView(request, deviceID):
    # the activity for a single device
    activity = services.getActivitiesFor(deviceID)
    template = 'detail.html'
    
    profile = services.getProfile(request.COOKIES['token'])
    org = profile[0].organisation
    site = services.getSites(org)

    temperatures = services.getLineData('temperature', activity)
    timestamps = services.getLineData('datetime', activity)
    vibrations = services.getLineData('vibrations',activity)
    cashAmount = services.getLineData('cashAmount',activity)
    cashDeposits = services.getLineData('cashDeposits',activity)
    humidity = services.getLineData('humidity',activity)
    downloadSpeed = services.getLineData('downloadSpeed',activity)
    paperLevel = services.getLineData('paperLevel', activity)
    transactionSpeed = services.getLineData('transactionSpeed', activity)

    context = {
        'activity':activity, 'deviceID':deviceID,
        'temperatures':temperatures, 'timestamps':timestamps,
        'vibrations':vibrations, 'cashAmount': cashAmount,
        'cashDeposits':cashDeposits, 'transactionSpeed':transactionSpeed,
        'humidity':humidity, 'downloadSpeed':downloadSpeed,
        'paperLevel':paperLevel, 'site': site,
        'profile': profile
    }
    return render(request, template, context=context)


def loginView(request):
    template = 'login.html'
    return render(request, template)

def registerView(request):
    template = 'register.html'
    organisations = services.getOrganisations()
    context = {'organisations': organisations}
    return render(request, template, context=context)


def verifyLoginView(request):
    username = request.POST.get('username')
    password = request.POST.get('password')

    token = authentication.getToken(username, password)
    try:
        if token['token']:
            response = redirect('application:home')
            response.set_cookie(key='token', value=token['token'])
            return response
    except:
        messages.add_message(request, messages.ERROR, 'Invalid username or password')
        return redirect('application:login')

def verifyRegisterView(request):
    username = request.POST.get('username')
    password = request.POST.get('password')
    organisation = request.POST.get('organisation')
    province = request.POST.get('province')
    email = request.POST.get('email')

    response = services.registerUser(
        username, password,
        organisation, province,
        email
    )

    if response == True:
        messages.add_message(request, messages.SUCCESS, 'You can now login')
    else:
        messages.add_message(request, messages.ERROR, 'Failed to register')

    return redirect('application:login')

def logoutView(request):
    response = redirect('application:login')
    response.delete_cookie('token')
    return response

@authentication.login_required
def redirectView(request):
    return redirect('application:home')

@authentication.login_required
def createDevice(request):
    deviceID = request.POST.get('deviceID')
    deviceName = request.POST.get('deviceName')
    site = request.POST.get('site')
    location = request.POST.get('location')
    next = request.POST.get('next', '/')
    profile = services.getProfile(request.COOKIES['token'])
    org = profile[0].organisation
    
    response = services.manipulateAsset(
        services.getSites(org), deviceID,
        deviceName, site,
        location
        )

    try:
        if response['error']:
            messages.add_message(request, messages.ERROR, 'Failed to create device.')
    except:
        messages.add_message(request, messages.SUCCESS, 'Successfully created device')
        
    return HttpResponseRedirect(next)

@authentication.login_required
def updateDevice(request):
    deviceID = request.POST.get('deviceID')
    deviceName = request.POST.get('deviceName')
    site = request.POST.get('site')
    location = request.POST.get('location')
    next = request.POST.get('next', '/')
    profile = services.getProfile(request.COOKIES['token'])
    org = profile[0].organisation
    
    response = services.manipulateAsset(
        services.getSites(org), deviceID,
        deviceName, site,
        location, update=True
        )

    try:
        if response['error']:
            messages.add_message(request, messages.ERROR, 'Failed to update device.')
    except:
        messages.add_message(request, messages.SUCCESS, 'Successfully Updated device')
    
    return HttpResponseRedirect(next)

@authentication.login_required
def newMessage(request):
    time = str(datetime.now())
    message = request.POST.get('message')
    profile = services.getProfile(request.COOKIES['token'])
    username = profile[0].username
    response = services.sendMessage(message, username, time)
    return redirect('application:home')