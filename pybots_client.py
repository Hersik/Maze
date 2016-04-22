# -*- coding: utf-8 -*-
"""
Created on Sat Apr 16 20:43:08 2016
Quest: Hl. program pro pripojení a ovládání pybots
"""
###############################################################################
import json
import http.client
from pprint import pprint
from urllib.parse import urlencode
from gen.path_generator import moves, objecttomap, show, find_players
#http://hroch.spseol.cz:44822/init
#zkouska = MyBot.post('/action', bot_id=MyBot.bot_id, 
#                       action=bot_path[x]).get('state')
###############################################################################

class Bot:

    def __init__(self, host='localhost', port='44822'):
        self.host=host
        self.port=port
        self.conn=http.client.HTTPConnection(host, port)
        self.conn.request("GET", "/init")
        resp=self.conn.getresponse()
        if resp.status == 200:
            data=resp.read().decode('UTF-8')
            data=json.loads(data)
            self.bot_id = data['bot_id']
        else:
            print(resp.status, resp.reason)
            print()
            pprint(resp.getheaders())
            print()
            print(resp.read().decode('UTF-8'))
            raise Exception("Hru se nepodařilo založit")

    def get(self, path, **param):
        enc_param=urlencode(param)
        self.conn.request('GET', '{}?{}'.format(path, enc_param))
        resp=self.conn.getresponse()
        return json.loads(resp.read().decode('UTF-8'))

    def getmap(self):
        self.conn.request("GET", "/game/{}".format(self.bot_id))
        resp=self.conn.getresponse()
        return json.loads(resp.read().decode('UTF-8'))['map']
    
    def getdata(self):
        self.conn.request("GET", "/game/{}".format(self.bot_id))
        resp=self.conn.getresponse()
        return json.loads(resp.read().decode('UTF-8'))['game_info']        
        
    def post(self, path, **param):
        enc_param=urlencode(param)
        headers={"Content-type": "application/x-www-form-urlencoded",
                   "Accept": "text/plain, application/json"}
        self.conn.request("POST", path, enc_param, headers)
        resp=self.conn.getresponse()
        return json.loads(resp.read().decode('UTF-8'))

    def end_connection(self):
        self.conn.close()

if __name__ == '__main__':
    MyBot = Bot('hroch.spseol.cz')
    data = MyBot.getdata()
    print(data)
    informations = MyBot.getmap()
    print(informations)
    informations = objecttomap(informations)
    bot_path=moves(labyrint=informations[0],location=informations[-1], 
               start = informations[1])
    print(bot_path, len(bot_path))
    for x in range(0,len(bot_path)):    
        responce = MyBot.post('/action', bot_id=MyBot.bot_id, 
                              action=bot_path[x])
        if responce["state"] == "game_won":
            print(responce["state"])
            break
        else:
            print(responce["state"])
            print(find_players(responce["game"]["map"]))
    MyBot.end_connection()