import discord
import urllib.request
import requests
import json
import sys
import os
class Session:
    def __init__(self):
        """
        Init of Sessions
        """
        self.apiKey="None"
        self.version=1
        self.logged=False
        self.lang="None"
        self.gif=False
        self.getApiUrl()
    def getApiUrl(self):
        try:
            page = urllib.request.urlopen("https://gist.githubusercontent.com/CR-crossplay/17d6c448202400bdccad7e1bc1466558/raw/9936ebd2aa9a7f001e3256940702a74c84e60d9f/api_url.txt")
            self.apiUrl=page.read().decode('utf-8')
        except:
            raise ValueError('Unable to get API URL')
    def setApiKey(self,new_api_key:str=""):
        if new_api_key=="": return "{!}Please give an api key{!}"
        try:
            res=requests.get(self.apiUrl+f'/v{str(self.version)}/user?apiKey={new_api_key}')
            if res.status_code==200:
                self.apiKey=new_api_key
                self.logged=True
                return "{*}Connected and Logged in{*}"
            else:
                self.logged=False
                return "{!}Wrong Api Key{!}"
        except Exception as err:
            self.logged=False
            return "{?} Can't connect to the API {?}"
    def setLang(self,new_lang:str=""):
        if new_lang=="": return "{!} Please give a language {!}"
        try:
            res=requests.get('http://'+self.apiUrl+f':5000/v{str(self.version)}/available_langs')
            data=json.loads(res.text)
            available_langs=[e for e in data['langs'].split(",")]
            if new_lang in available_langs: 
                self.lang=new_lang
                return "{*}Language set to "+new_lang+"{*}"
            else:
                return "{!} Unknown Language {!}"
        except Exception as err: 
            return "{!} An error occured {!}"

    
    def add_ad(self,embed:discord.Embed):
        if self.apiKey=="None":
            embed.add_field(
                name="Spotlight API - Error Logs",
                value="You hasn't logged your session before asking for an ad. Default message."
            )
            return embed
        if self.lang=="None":
            embed.add_field(
                name="Spotlight API - Error Logs",
                value="You hasn't set the language of your session before asking for an ad."
            )
            return embed
        if self.logged==False:
            embed.add_field(
                name="Spotlight API - Error Logs",
                value="You hasn't logged your session before asking for an ad. Default message."
            )
            return embed
        try:
            res=requests.get(self.apiUrl+f'/v{str(self.version)}/ad/get?apiKey={self.apiKey}&language={self.lang}&gif={self.gif}')
            data=json.loads(res.text)
            if data['all_ok']:
                embed.add_field(
                    name=data['name'],
                    value=data['value'],
                    inline=False
                )
                if self.gif and 'gif' in data:
                    embed.set_image(url=data['gif'])
            else:
                embed.add_field(
                    name="Spotlight API - An Error Occured",
                    value=f"Seems like we didn't have any ad for you or an error occured\n Status Code : {str(data.status_code)} \n Help : {str(data.help)}"
                )
            return embed
        except Exception as err: 
            return embed
actual_session=Session()

def setApiKey(apiKey:str=''):
    """set the apiKey of your Session"""        
    return actual_session.setApiKey(apiKey)
def setLang(newLang:str=''):
    """set the language of the ads received"""
    return actual_session.setLang(newLang)
def add_ad(embed:discord.Embed):
    return actual_session.add_ad(embed)