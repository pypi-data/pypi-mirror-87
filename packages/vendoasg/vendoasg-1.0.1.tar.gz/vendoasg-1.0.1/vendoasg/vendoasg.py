#! python
#-*- coding: utf-8 -*-

import requests
import json

class Vendo:

    def __init__(self, url_api):
        self.setHeader({'Content-Type' : 'application/json', "Content-Length" : "length"})
        self.setApi(url_api)

    def setApi(self,api_url):
        self.API_URL = api_url

    def setHeader(self, api_header):
        self.API_HEADER = api_header

    def getJson(self,request_url, request_data):
        req_url = self.API_URL + request_url
        json_data = requests.post(req_url, json=request_data, headers=self.API_HEADER)
        return json_data.json()

    def logInApi(self, api_login, api_pswd):
        jsonData = self.getJson(
            "/json/reply/Autoryzacja_Zaloguj",
            {"Model":{"Login":api_login,"Haslo":api_pswd}})
        self.VENDO_TOKEN = jsonData["Wynik"]["Token"]

    def logOutApi(self):
        jsonData = self.getJson(
            "/json/reply/Autoryzacja_Wyloguj",
            {"Token":self.VENDO_TOKEN})
        
    def loginUser(self,user_login, user_pswd):
        jsonData = self.getJson(
            "/json/reply/Autoryzacja_ZalogujUzytkownikaVendo",
            {"Token":self.VENDO_TOKEN,"Model":{"Login":user_login,"Haslo":user_pswd}})
        self.USER_TOKEN = jsonData["Wynik"]["Token"]
    
    def logOutUser(self):
        jsonData = self.getJson(
            "/json/reply/WylogujUzytkownikaVendo",
            {"Token": self.USER_TOKEN})