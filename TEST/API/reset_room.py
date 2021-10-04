import json
import requests
from get_room import room_id
from get_room import url_enter_selected_room
from get_room import url_get_room
# from get_room import session
from get_room import result

##対戦部屋へ全ユーザーをログアウト

delete_data ={
    "id": -1,
    "state": -1,
    # "player1":null,
    "player2":"A2"
}
url_reset_room = url_get_room  + "/" + str(room_id)
dele_data1 ={
    "player_id": "f30491d7-d862-4535-beab-077d682cb31f",
    "room_id": room_id
}
# +"/" + str(room_id)
# logout_post1 = session.delete(url_reset_room)
# logout_post1 = session.delete(url_reset_room)
# session.close()
logout_room =requests.get(url_get_room)
ll=requests.delete(url_get_room,data=dele_data1)
# logout_post2 = session.post(url_get_room,data=json.dumps(delete_data))
# print(logout_post1.status_code)
# print(logout_post1.json)
# print(logout_post2.status_code)
# print(logout_post2.json)
# result = session.get(url_get_room)
print(ll.status_code)
print(ll.json())