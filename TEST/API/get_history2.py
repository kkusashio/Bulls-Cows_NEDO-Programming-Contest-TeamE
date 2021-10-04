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
his_url2 = url_enter_selected_room + "/players/" + user_name2 + "/table"
his_post2 = session.get(his_url2)
print(his_post2.status_code)
print(his_post2.json())
