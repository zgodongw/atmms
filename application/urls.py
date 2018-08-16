from django.urls import path

from . import views

app_name = "application"

urlpatterns = [
    path(
        '',
        views.redirectView,
        name='index'
        ),
    path(
        'home/',
        views.homeView,
        name='home'
        ),
    path(
        'devices/<str:place>',
        views.listView,
        name='list'
        ),
    path(
        'devices/create/',
        views.createDevice,
        name='create-device'
        ),
    path(
        'devices/update/',
        views.updateDevice,
        name='update-device'
        ),
    path(
        'activity/<str:deviceID>/',
        views.detailView,
        name='detail'
        ),
    path(
        'login/',
        views.loginView, 
        name='login'
        ),
    path(
        'register/',
        views.registerView, 
        name='register'
        ),
    path(
        'verify-login/',
        views.verifyLoginView, 
        name='verify'
        ),
    path(
        'verify-register/',
        views.verifyRegisterView, 
        name='verify-register'
        ),
    path(
        'logout/',
        views.logoutView, 
        name='logout'
        ),
    path(
        'sendmessage',
        views.newMessage,
        name='create-message'
        )
]