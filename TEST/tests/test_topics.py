import requests
import json

##対戦部屋の情報の取得
base_url = "https://damp-earth-70561.herokuapp.com/rooms"
room_id = 5002
url_get_room = base_url + "/" + str(room_id)
session = requests.Session()
response_result = session.get(url_get_room)

url_get_topics = url_get_room + "/topics"

topics = requests.get(url_get_topics)
print(topics)
print(response_result.status_code)
print(response_result.json())

##対戦部屋へユーザー1を登録
headers = {"Content-Type":"application/json"} #json format
url_enter_room = base_url
post_data ={
    "player_id": "f30491d7-d862-4535-beab-077d682cb31f",
    "room_id": room_id
}
result_post = session.post(url_enter_room,headers=headers,json=post_data)
print(result_post.status_code)
print(result_post.json)

##Number guess function
def get_guess_num_auto():
    guess_info = {
        "player_id": "string",
        "guess": "string"
    }
    r = requests.get(url_get_topics,params=guess_info)
    print(r.status_code)
    print(r.json())

get_guess_num_auto()