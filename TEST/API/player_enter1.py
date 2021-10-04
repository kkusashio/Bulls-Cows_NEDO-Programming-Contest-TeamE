import json
import requests
from get_room import room_id
from get_room import url_get_room
from get_room import session

##対戦部屋へユーザー1を登録
user_name1 = "E"
user_id1 = "f30491d7-d862-4535-beab-077d682cb31f"
headers = {"Content-Type":"application/json"}
post_data1 ={
    "player_id": user_id1,
    "room_id": room_id
}
romm_enter1 = session.post(url_get_room,headers=headers,json=post_data1)
# print(result_post1.status_code)
# print(result_post1.json())