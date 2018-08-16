import os

class Organisation():
    def __init__(self, id, name):
        self.id = id
        self.name = name

class Site():
    def __init__(self, place, *args, **kwargs):
        self.id = args[0]
        self.place = place
        self.province = args[1]

class Asset():
    def __init__(self, id, deviceName, deviceID, location, site, *args, **kwargs):
        self.id = id
        self.deviceName = deviceName
        self.deviceID = deviceID
        self.location = location
        self.site = site

class Activity():
    def __init__(self, *args, **kwargs):
        self.datetime = args[0]
        self.temperature = args[1]
        self.vibrations = args[2]
        self.cashAmount = args[3]
        self.cashDeposits = args[4]
        self.transactionSpeed = args[5]
        self.humidity = args[6]
        self.downloadSpeed =args[7]
        self.paperLevel = args[8]

class Message():
    def __init__(self, message, username, timestamp):
        self.message = message
        self.username = username
        self.timestamp = timestamp

class Profile():
    def __init__(self, id, username, organisation, province, color):
        self.id = id
        self.color = color
        self.username = username
        self.organisation = organisation
        self.province = province

class User():
    def __init__(self, id, username):
        self.id = id
        self.username = username