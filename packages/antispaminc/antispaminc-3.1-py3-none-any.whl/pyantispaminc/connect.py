# Copyright (C) 2020 AntiSpam, Inc. <http://antispaminc.tk/>
#
#                    GNU GENERAL PUBLIC LICENSE
#                      Version 3, 29 June 2007

# Copyright (C) 2020 AntiSpam, Inc. <http://antispaminc.tk/>
# Everyone is permitted to copy and distribute verbatim copies
# of this license document, but changing it is not allowed.

import json
import os
from datetime import datetime, timedelta
import requests
from .class_types import Antispamclass

class Connect():
    '''
    LoL
    '''

    def __init__(self, token=None):
        self.token = token
        self.base = 'http://antispaminc.tk/'
        if token is None:
            raise ApiError("You must supply a valid AntispamInc Api Key, Contact @AntispamIncBot To Get One")
    def ban(self, user_id, reason):
        token = self.token
        userid = user_id
        reason_is = reason
        urlis = self.base + f'/ban/?userid={userid}&reason={reason_is}&token={token}'
        lmao = requests.get(url=urlis).json()
        if lmao['error'] == True:
            raise ApiError(f"Something Went Wrong \nError : {lmao['full']}")
        else:
            return lmao
                           
    def unban(self, user_id):
        token = self.token
        userid = user_id
        urlim = self.base + f'/unban/?userid={userid}&token={token}'
        lmao = requests.get(url=urlim).json()
        if lmao['error'] == True:
            raise ApiError(f"Something Went Wrong \nError : {lmao['full']}")
        else:
            return lmao
                                  
    def new_token(self, token):
        tokenz = token
        secret_token = self.token
        url_2 = self.base + f'/newtoken/?token={tokenz}&secrets={secret_token}'
        star = requests.get(url=url_2).json()
        if star['error'] == True:
            raise ApiError(f"Something Went Wrong \nError : {star['full']}")
        else:
            return star
    def is_banned(self, user_id):
        token = self.token
        userid = user_id
        is_it = {
            'token': token,
            'userid': userid
        }
        urlz = self.base + '/info/'
        seds = requests.post(url=urlz, data=is_it).json()
        if seds['error'] == True:
            raise ApiError('Something Went Wrong. \nError' + seds['full'])
        else:
            lol = seds['banned']
            return Antispamclass(**seds)

class ApiError(Exception):
    pass
