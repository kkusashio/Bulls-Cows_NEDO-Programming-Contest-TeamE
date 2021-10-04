## URLの導入
import json
import requests
url = "https://damp-earth-70561.herokuapp.com"
# save cookies for post_data for first request
session = requests.Session()

##対戦部屋の情報の取得
room_id =5002
url_get_room = url + "/rooms/" + str(room_id)
url_get_topics = url_get_room + "/topics"
result = session.get(url_get_room)
topics = requests.get(url_get_topics)
print(topics)
print(result.status_code)
print(result.json())

##対戦部屋へユーザーを登録
headers = {"Content-Type":"application/json"}
url_enter_room = url + "/rooms"
post_data ={
    "player_id": "f30491d7-d862-4535-beab-077d682cb31f",
    "room_id": room_id
}
result_post = session.post(url_enter_room,headers=headers,json=post_data)
print(result_post.status_code)
print(result_post.json)

##Topicの作成
