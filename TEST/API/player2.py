# add additional functions
#coding: UTF-8
from typing import List,Tuple,Optional
import json
import random
import requests
from datetime import datetime
import time
import threading
from player1 import ROOM_ID

import argparse


numberchoice = ['0','1','2','3','4','5','6','7','8','9','a','b','c','d','e','f']

HIT_NUM = 0
BLOW_NUM = 0
MAX_STAGE = 100
USER1_NAME = 'E'
USER1_ID = 'f30491d7-d862-4535-beab-077d682cb31f'
USER2_NAME = 'E2'
USER2_ID ='46711285-133d-40b6-93ae-e93d9404fb43'
URL = "https://damp-earth-70561.herokuapp.com"
# ROOM_ID = 5007
ROOM_URL = URL + "/rooms/" + str(ROOM_ID)
ENTER_URL = URL + "/rooms"
HIDDEN_URL = ROOM_URL + "/players/" + USER2_NAME + "/hidden"
HISTORY_URL = ROOM_URL + "/players/" + USER2_NAME + "/table"
GUESS_URL = HISTORY_URL + "/guesses"
session = requests.Session()

class game_prepare:
    """数当てゲーム
    手入力で遊ぶモード、線形探索で解くモード、分割統治で解くモード
    :param int min_ans:　出題範囲の下限値
    :param int max_ans:　出題範囲の上限値
    :param int max_stage:　回答回数の制限
    :param int ans:　出題値
    :param int stage: 現在の回答回数
    :param List[int] history: 回答履歴
    :param int right:　分割統治法の探索範囲下限
    :param int left:　分割統治法の探索範囲上限
    """
    def __init__(self, hit_num:int=0, blow_num:int=0, max_stage:int=5,guess: Optional[int] = None) -> None:
        """コンストラクタ
        :param int hit_ans:　一回hit数
        :param int blow_ans:　一回blow数
        :param int max_stage:　回答回数制限指定
        :rtype: None
        :return: なし
        """
        self.hit_num = hit_num
        self.blow_num = blow_num
        self.max_stage = max_stage
        self.stage = 0
        self.order = 0
        self.wait = 0
        self.opponent_check = 0
        self.pre_e = 0
        self.hid = 0
        self.turn = 0
        self.pre_h = 0
        self.pre_s = 0
        self.op_pre = 0
        
        self.g_history: List[int] = []
        self.h_history: List[int] = []
        self.b_history: List[int] = []
        self.history: Tuple[List[int],List[int],List[int]] = [self.g_history,self.h_history,self.b_history]
        self.secret = 0
        self.guess = 0

        # if guess is not None:
        #     self.guess =guess
        # else:
        #     self.guess = self._define_answer()

    def run(self) ->Tuple[List[int],List[int],List[int]]:
        self._start_game_auto()
        while self.hit_num != 5:
            self._play_contine()
            return self.history
        print("winner generated")

    # def run(self,mode) ->Tuple[int,Tuple[List[int],List[int],List[int]]]:
    #     """数当てゲームを実行するランナー
        
    #     :param str mode: ゲームの実行モード("manual", "linear", "binary")
    #     :rtype: Tuple[int,List[int]]
    #     :return: 回答回数,回答履歴
    #     """
    #     if mode == "linear":
    #         self._play_game_auto_rand()
    #     # elif mode == "binary":
    #     #     self._play_game_auto_binary()
    #     else:
    #         self._play_game_manual()
    #     self._show_result()
    #     return self._get_history()
    
    def _play_contine(self) -> None:
        if self.turn == -1:
            time.sleep(5)
            self._self_opponent_status_check()
            if self.pre_h == 1 and self.pre_s == 0:
                
                self._self_opponent_status_check()
            else:
                timer.cancel()
                self._guess_gene()
            
        elif self.turn == 1:
            self._guess_gene()
            time.sleep(5)
            self._self_opponent_status_check()
            if self.pre_s == 1:
                timer.cancel()
                self._get_history()
            else:
                
                self._self_opponent_status_check()



    def _start_game_auto(self)->None:
        self._pre_room()
        if self.order == 1:
            self._enter_room()
            if self.wait == 1:
                time.sleep(5)
                self._self_opponent_status_check()
                if self.pre_e == 1:
                    timer.cancel()
                    self._hidden_gene()
                else:
                    
                    self._self_opponent_status_check()
            elif self.wait == 2:
                self._hidden_gene()
                if self.hid == 1:
                    time.sleep(5)
                    self._self_opponent_status_check()
                    if self.pre_h == 1 and self.pre_s == 0:
                        
                        self._self_opponent_status_check()
                    else:
                        timer.cancel()
                        self._guess_gene()
                    
                elif self.hid == 2:
                    self._guess_gene()
                    time.sleep(5)
                    self._self_opponent_status_check()
                    if self.pre_s == 1:
                        timer.cancel()
                        self._get_history()
                    else:
                        
                        self._self_opponent_status_check()
                        
                else:
                    print("error in guess input")
                    
            else:
                print("error in hidden number generation")
                
        else:
            print("error in entering room")
            
    



    def _self_opponent_status_check(self):
        check_enter_url = ROOM_URL
        check_enter_info = session.get(check_enter_url)
        check_enter_info = json.loads(check_enter_info.text)
        if check_enter_info["player1"] is not None and check_enter_info["player2"]:
            self.pre_e = 1
        else:
            self.pre_e = 0
        check_hidden_url  = HIDDEN_URL
        headers = {"Content-Type":"application/json"}
        secret_data1 ={
            "player_id": USER2_ID,
            "hidden_number":  self.secret
        }
        # check_hidden_info = session.get(check_hidden_url)
        check_hidden_info = session.post(check_hidden_url, headers=headers, json=secret_data1)
        print(check_hidden_info.text)
        hidden_gene_info = json.loads(check_hidden_info.text)
        if hidden_gene_info["detail"] == 'you can not select hidden':
            self.pre_h = 1
        else:
            self.pre_h = 0
        check_guess_url = GUESS_URL
        guess_data1 ={
            "player_id": USER2_ID,
            "guess": self.guess #args.ans
        }
        check_guess_info = session.post(check_guess_url,headers=headers,json=guess_data1)
        check_guess_info = json.loads(check_guess_info.text)
        if  check_guess_info["detail"] == 'opponent turn':
            self.pre_s = 1
            self.op_pre = 0
        elif check_guess_info["now_player"] == 'E':
            self.pre_s = 1
            self.op_pre = 0
        else:
            self.pre_s = 0
            self.op_pre = 1




    def _pre_room(self,room_id:int = ROOM_ID) -> int:
        room_url = ROOM_URL
        room_info =session.get(room_url)
        if room_info.status_code == 200 or room_info.status_code == 400:
            order_of_player = json.loads(room_info.text)
            if order_of_player['player1'] =='E2':
                self.order = 1
                print("You are already in room {}, you are player1, your name is {}".format(room_id,order_of_player['player1']))
                print(room_info.text)
            elif order_of_player['player2'] == 'E2':
                self.order = 1
                print("You are already in room {}, you are player2, your name is {}".format(room_id,order_of_player['player2']))
            elif order_of_player['player1'] is  None or order_of_player['player2'] is None:
                c_r =input("You are not in this room now, but you can enter, y/n ->")
                if c_r == 'y':
                    room_id = input("Please enter room id ->")
                    self.order = 1
                elif c_r == 'n':
                    print("Program stopped")
                    self.order = -1
                else:
                    c_r = input("Wrong answer, please type in y/n ->")
                    self.order = -1
            else:
                self.order = -1
                room_id = input("You cannot enter this room, please change another room ->")
        else:
            self.order = -2
            # room_id = input("Enter room {} failed, please try again, or change room id",room_id)
            print("Enter room {} failed, please try again, or change room id",room_id)
        
    

    def _enter_room(self,room_id:int = ROOM_ID) ->None:
        enter_url = ENTER_URL
        headers = {"Content-Type":"application/json"}
        post_data1 = {
            "player_id": USER2_ID,
            "room_id": room_id
        }
        enter_room = session.post(enter_url,headers=headers,json=post_data1)
        enter_info = session.get(enter_url + '/' + str(room_id))
        # room_check = enter_info.json()
        room_check = json.loads(enter_info.text)
        if enter_room.status_code == 200 or enter_room.status_code == 400:
            if room_check['state'] == 1 and room_check['player1'] == 'E2':
                self.wait = 1
                print("You are sucessfully entered room {},you are player1, please wait for another player".format(room_id))
                self.opponent_check = 0
            elif room_check['state'] == 1 and room_check['player2'] == 'E2':
                self.wait = 1
                print("You are sucessfully entered room {},you are player2, please wait for another player".format(room_id))
                self.opponent_check = 0
            elif room_check['state'] == 2 and room_check['player1'] == 'E2':
                self.wait = 2
                print("You are sucessfully entered room {},you are player2, game will start soon".format(room_id))
                self.opponent_check = 1
            elif room_check['state'] == 2 and room_check['player2'] == 'E2':
                self.wait =2
                print("You are sucessfully entered room {},you are player2, game will start soon".format(room_id))
                self.opponent_check = 1
            else:
                self.wait =-1
                print("You failed entering room {},please try again".format(room_id))
        else:
            self.wait = -2
            print("Enter room failed, please try again, or change room id")
    

    def _hidden_gene(self) -> int:
        hidden_url = HIDDEN_URL
        headers = {"Content-Type":"application/json"}
        secret = random.sample(numberchoice,5)
        self.secret = "".join(secret)
        secret_data1 ={
            "player_id": USER2_ID,
            "hidden_number": self.secret #args.ans
        }
        hidden_post = session.post(hidden_url,headers=headers,json=secret_data1)
        print(hidden_post.text)
        # hidden_gene_info = hidden_post.json()
        hidden_gene_info = json.loads(hidden_post.text)
        if hidden_post.status_code == 200 :
            if hidden_gene_info['selecting'] == 'True':
                self.hid = 1
                print("Room {} :Secret generated, you are player1, please wait for opponent secret generation".format(ROOM_ID))
                self.opponent_check = 0
            elif hidden_gene_info['selecting'] == 'False':
                self.hid = 2
                print("Room {} :Secret generated, you are player2, now player1 will guess first".format(ROOM_ID))
                self.opponent_check = 1
            else:
                self.hid = -1
                print("Failed generate secret, please try again")
        elif  hidden_post.status_code == 400:
            if hidden_gene_info['detail'] == 'you can not select hidden':
                self.hid = 2
                print("Room {} :Secret already generated, you are player2, now player1 will guess first".format(ROOM_ID))
                self.opponent_check = 1
            else:
                print("Error in hidden response")
        else:
            self.hid = -2
            print("Generate hidden number failed, please try again")
    

    def _guess_gene(self) ->None:
        guess_url = GUESS_URL
        headers = {"Content-Type":"application/json"}
        guess = random.sample(numberchoice,5)
        self.guess = "".join(guess)
        guess_data1 ={
            "player_id": USER2_ID,
            "guess": self.guess #args.ans
        }
        guess_post1 = session.post(guess_url,headers=headers,json=guess_data1)
        # guess_gene_info = guess_post1.json()
        guess_gene_info = json.loads(guess_post1.text)
        if guess_post1.status_code == 200 :
            if guess_gene_info['now_player'] == 'E':
                self.turn = -1
                print("Opponent turn, please wait")
            else:
                self.turn = 1
                if guess_gene_info['guesses'][-1] == self.guess:
                    self.history[0].append(self.guess)
                else:
                    print("Failed generate guess, please try again")
        elif guess_post1.status_code == 400:
            if guess_gene_info['detail'] == 'opponent turn':
                self.turn = -1
                print("Opponent turn, please wait")
            else:
                print("Error in guess response")
        else:
            print("Generate guess failed, please try again")


    def _get_history(self) -> Tuple[int,Tuple[List[int],List[int],List[int]]]: 
        his_url = HISTORY_URL
        his_info = session.get(his_url)
        # his_get = his_info.json()
        his_get = json.loads(his_info.text)
        if his_info.status_code == 200:
            print(his_info.json())
            # if his_info['winner'] is not None:
            if his_get['table'][-1]['guess'] == self.guess:
                self.stage +=1
                self.hit_num = his_get['table'][-1]['hit']
                self.blow_num = his_get['table'][-1]['blow']
                self.history[1].append(self.hit_num)
                self.history[2].append(self.blow_num)
                return self.stage, self.history
            else:
                print("History unmatch, please try again")
            # else:
            #     print("Winner has be generated, Congratulations!!{}!!, you will for {} times game".format(his_info['winner'],his_info['game_end_count']))
        else:
            print("Get history failed, please try again")

    




def get_parser() ->argparse.Namespace:
    """コマンドライン引数を解析したものをもつ

    :rtype:argparse.Namespace
    :return: コマンド値
    """
    parser=argparse.ArgumentParser(description='数当てゲーム')
    parser.add_argument('--hit_num',default=0)
    parser.add_argument('--blow_num',  default=0)
    parser.add_argument('--max_stage', default=5)
    parser.add_argument("--guess")
    # parser.add_argument('--mode', default="manual")
    args=parser.parse_args()
    return args


# def timer(n):
#     while True:
#         print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
#         time.sleep(n)

def fun_timer():
    global timer
    timer = threading.Timer(5.5,fun_timer)
    timer.start()

def main() ->None:
    """数当てゲームのメイン
    :rtype:None
    :return: なし
    """
    args=get_parser()
    hit_num = int(args.hit_num)
    blow_num = int(args.blow_num)
    max_stage = int(args.max_stage)
    # mode = args.mode
    timer = threading.Timer(2,fun_timer)
    timer.start()


    # runner = game_prepare._play_game_auto()
    # print(args.ans)
    if args.guess is not None:
        guess = int(args.guess)
        runner =game_prepare(hit_num=hit_num,blow_num=blow_num,max_stage=max_stage,guess=guess)
    else:
        runner = game_prepare(hit_num=hit_num,blow_num=blow_num,max_stage=max_stage)
    history = runner.run()

if __name__ == '__main__':
    main()


