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
secret_url = url_enter_selected_room + "/players/" + user_name1 + "/hidden"
guess_url = url_enter_selected_room + "/players/" + user_name1 + "/table/guesses"
numberchoice_g1 = ['0','1','2','3','4','5','6','7','8','9','a','b','c','d','e','f']

secret = random.sample(numberchoice_g1,5)
secret = "".join(secret)
# args=collection.get_parser()
# print(args.ans)
secret_data1 ={
    "player_id": user_id1,
    "hidden_number": secret #args.ans
}
print(secret)
secret_post1 = session.post(secret_url,headers=headers,json=secret_data1)
print(secret_post1.status_code)
print(secret_post1.json())


guess = random.sample(numberchoice_g1,5)
guess = "".join(guess)
guess_data1 ={
    "player_id": user_id1,
    "guess": guess #args.ans
}
print(guess)
guess_post1 = session.post(guess_url,headers=headers,json=guess_data1)
print(guess_post1.status_code)
print(guess_post1.json())

