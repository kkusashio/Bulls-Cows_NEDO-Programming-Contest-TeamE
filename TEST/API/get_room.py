import json
import requests

# from TEST.API.player1 import ROOM_ID
url = "https://damp-earth-70561.herokuapp.com"
session = requests.Session()
ROOM_ID=5009

##対戦部屋の情報の取得
room_id =ROOM_ID
url_enter_selected_room = url + "/rooms/" + str(room_id)
url_get_room = url + "/rooms"
result = session.get(url_enter_selected_room)
print(result.status_code)
print(result.json())


