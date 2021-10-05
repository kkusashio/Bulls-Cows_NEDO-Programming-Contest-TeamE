import json
import random
import requests
# from TEST.API.Guess import NumberGuess
from get_room import room_id, session
from get_room import url_get_room, url_enter_selected_room
from player_enter1 import user_id1,user_name1
from player_enter2 import user_id2, user_name2
import Guess
import collection

##ユーザー1の推測数字を登録
headers = {"Content-Type":"application/json"}
his_url = url_enter_selected_room + "/players/" + user_name1 + "/table"
his_post1 = session.get(his_url)
#print(his_post1.status_code)
#print(his_post1.json())

dict=his_post1.json()

print('room_id: ', his_post1.json().get('room_id'))
print('state: ', his_post1.json().get('state'))
print('now_player: ', his_post1.json().get('now_player'))
print('table: ', his_post1.json().get('table'))
print('opponent_table: ', his_post1.json().get('opponent_table'))
print('winner: ', his_post1.json().get('winner'))
print('game_end_count: ', his_post1.json().get('game_end_count'))