import json
import random
import requests
# from TEST.API.Guess import NumberGuess
from get_room import ROOM_ID, session
from get_room import url_get_room, url_enter_selected_room
from player_enter1 import user_id1,user_name1
from player_enter2 import user_id2, user_name2
import Guess
import collection

##ユーザー1のsecretを登録
headers = {"Content-Type":"application/json"}
secret_url = url_enter_selected_room + "/players/" + user_name2 + "/hidden"
secret_id ={
    "room_id": ROOM_ID,
    "player_name": user_name2

}
numberchoice_s2 = ['0','1','2','3','4','5','6','7','8','9','a','b','c','d','e','f']
secret = random.sample(numberchoice_s2,5)
secret = "".join(secret)
# args=collection.get_parser()
# print(args.ans)
secret_data2 ={
    "player_id": user_id2,
    "hidden_number": secret #args.ans
}
# print(secret)
# secret_post2 = session.post(secret_url,headers=headers,json=secret_data2)
# print(secret_post2.status_code)
# print(secret_post2.json())

#ユーザー2のhidden登録の関数化
def _secret_generation2()->None:
    hidden_post2=session.post(secret_url,headers=headers,json=secret_data2)
    hidden_post_check2=json.loads(hidden_post2.text)
    if hidden_post2.status_code==200:
        if hidden_post_check2['selecting'] == 'True':
            print("game start after player 2 prepared for secret number,you are player1")
        elif hidden_post_check2['selecting'] == "False":
            print("all player prepared, game start in 5 seconds,you are player2")
        else:
            print("error happened in hidden number generation,please try again")
    else:
        print("error happened in hidden number generation,please try again")

_secret_generation2()