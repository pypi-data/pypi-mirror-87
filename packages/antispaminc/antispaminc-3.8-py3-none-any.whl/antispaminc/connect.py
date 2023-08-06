# Copyright (C) 2020 AntiSpam, Inc. <http://antispaminc.tk/>
#
#                    GNU GENERAL PUBLIC LICENSE
#                      Version 3, 29 June 2007

# Copyright (C) 2020 AntiSpam, Inc. <http://antispaminc.tk/>
# Everyone is permitted to copy and distribute verbatim copies
# of this license document, but changing it is not allowed.

import os
import requests
from .class_types import Antispamclass


class Connect():
    '''
    Class To Connect Your Token And Use It Efficiently.
    '''

    def __init__(self, token=None):
        self.token = token
        self.base = 'http://antispaminc.tk'
        lol = 'http://antispaminc.tk' + f'/tokencheck/?token={token}'
        hmmok = requests.get(url=lol).json()
        if hmmok['token_valid'] == False:
            raise TokenNotFound(token)
        else:
            pass

    def ban(self, user_id, reason):
        """
        :param user_id: User id of entity
        :param reason: reason of ban
        :return: Json Object
        Requires Dev Permission
        """
        token = self.token
        userid = user_id
        reason_is = reason
        urlis = 'http://antispaminc.tk' + f'/ban/?userid={userid}&reason={reason_is}&token={token}'
        omk = requests.get(url=urlis).json()
        if omk['error'] == True:
            raise RequestError(omk['full'])
        else:
            return omk

    def unban(self, user_id):
        """
        :param user_id: User id of entity to unban
        :return: json object if success else raises Exception
        """
        token = self.token
        userid = user_id
        urlim = 'http://antispaminc.tk' + f'/unban/?userid={userid}&token={token}'
        lmao = requests.get(url=urlim).json()
        if lmao['error'] == True:
            raise RequestError(lmao['error'])
        else:
            return lmao

    def new_token(self, tokeny):
        """
        :param token: Token which should be added
        :return: Json object if success else raises Exception
        """
        tokenz = tokeny
        secret_token = self.token
        url_2 = 'http://antispaminc.tk' + f'/newtoken/?token={tokenz}&secrets={secret_token}'
        star = requests.get(url=url_2).json()
        if star['error'] == True:
            raise RequestError(star['full'])
        else:
            return star

    def is_banned(self, user_id):
        """
        :param user_id: userid of entity
        :returns: Ban Class(Object)
        """
        token = self.token
        userid = user_id
        is_it = {
            'token': token,
            'userid': userid
        }
        urlz = 'http://antispaminc.tk' + '/info/'
        seds = requests.post(url=urlz, data=is_it).json()
        if seds['error'] == True:
            raise RequestError(seds['full'])
        else:
            return Antispamclass(**seds)


class BasicError(Exception):
    pass

class TokenNotFound(BasicError):
    def __init__(self, token) -> None:
        Exception.__init__(self, f"Your Token {token}, Is Invalid. Please Get From @AntispamIncBot")

class RequestError(BasicError):
    def __init__(self, errorfull) -> None:
        Exception.__init__(self, f"Something Went Wrong While Processing Your Request \nError: {errorfull}")


