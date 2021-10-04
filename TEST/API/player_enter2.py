import json
import requests
from get_room import room_id
from get_room import url_get_room
from get_room import session

##対戦部屋へユーザー2を登録
user_name2 = "E2"
user_id2 = "46711285-133d-40b6-93ae-e93d9404fb43"
headers = {"Content-Type":"application/json"}
post_data2 ={
    "player_id": user_id2,
    "room_id": room_id
}
room_enter2 = session.post(url_get_room,headers=headers,json=post_data2)
# print(result_post2.status_code)
# print(result_post2.json())