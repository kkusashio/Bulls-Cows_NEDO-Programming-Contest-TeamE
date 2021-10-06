import json
import requests
url = "https://damp-earth-70561.herokuapp.com"
session = requests.Session()

##対戦部屋の情報の取得
room_id =5003
url_enter_selected_room = url + "/rooms/" + str(room_id)
url_get_room = url + "/rooms"
result = session.get(url_enter_selected_room)
print(result.status_code)
print(result.json())


