# add additional functions
#coding: UTF-8
from typing import List,Tuple,Optional
import json
import random
import math
import requests
from datetime import datetime
import time
import threading

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
ROOM_ID = 5008
ROOM_URL = URL + "/rooms/" + str(ROOM_ID)
ENTER_URL = URL + "/rooms"
HIDDEN_URL = ROOM_URL + "/players/" + USER1_NAME + "/hidden"
HISTORY_URL = ROOM_URL + "/players/" + USER1_NAME + "/table"
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
        self.pre_E = 0
        self.op_pre = 0
        self.digits=5 #桁数
        self.numbers=16 #選択肢
        self.tries = 0 #トライ数
        self.hits = [] 
        self.blows = []
        self.guessed_numbers = [] #過去に予想したもの
        self.total_possibilities = math.factorial(self.numbers)/math.factorial(self.numbers-self.digits) #可能性の総数
        self.ans=[] #正解
        self.guess=[] #そのトライでの予測
        
        self.g_history: List[int] = [00000]
        self.h_history: List[int] = [0]
        self.b_history: List[int] = [0]
        self.history: Tuple[List[int],List[int],List[int]] = [self.g_history,self.h_history,self.b_history]
        # self.g_history: List[int] = self.history[0]
        # self.h_history: List[int] = self.history[1]
        # self.b_history: List[int] = self.history[2]
        # self.history: Tuple[List[int],List[int],List[int]] = [[],[],[]]
        self.secret = 0
        # self.guess = 0

        # if guess is not None:
        #     self.guess =guess
        # else:
        #     self.guess = self._define_answer()

    def run(self) ->Tuple[List[int],List[int],List[int]]:
        
        self._start_game_auto()
        self._get_history()
        while True:
            self._play_contine()
            if self._winner() == 1:
                print("winner generated")
                break
            else:
            # time.sleep(10)
                return self.history
            
            
        

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
        time.sleep(1)
        timer.cancel()
        while self.hit_num <5:
            self._guess_gene()
            self._get_history()
            if self.turn == 1:
                time.sleep(2)
                self._self_opponent_guess_check()
                
                
            else:
                if self.pre_h == 1 and self.pre_E == -1:
                    # time.sleep(10)
                    # timer.cancel()
                    self._guess_gene()
                    self._get_history()
                    
                else:
                    time.sleep(2)
                    self._self_opponent_guess_check()
            





    def _start_game_auto(self)->None:
        self._pre_room()
        if self.order == 1:
            self._enter_room()
            if self.wait == 1:
                time.sleep(2)
                self._self_opponent_enter_check()
                if self.pre_e == 1:
                    timer.cancel()
                    self._hidden_gene()
                else:
                    self._self_opponent_enter_check()
            elif self.wait == 2:
                self._hidden_gene()
                if self.hid == 1:
                    time.sleep(4)
                    timer.cancel()
                    self._guess_gene()
                    self._get_history()
                    self._self_opponent_hidden_check()
                    # if self.pre_h == 1 and self.pre_E == 1:
                    #     time.sleep(10)
                    #     timer.cancel()
                    # else:
                    #     self._self_opponent_hidden_check()
                    
                elif self.hid == 2:
                    self._guess_gene()
                    self._get_history()
                    self._self_opponent_guess_check()
                    # if self.pre_E == 1:
                    #     time.sleep(10)
                    #     timer.cancel()
                    # else:
                    #     self._self_opponent_guess_check()
                        
                else:
                    print("error in guess input")
                    
            else:
                print("error in hidden number generation")
                
        else:
            print("error in entering room")
            
    


    
    def _self_opponent_enter_check(self):
        check_enter_url = ROOM_URL
        check_enter_info = session.get(check_enter_url)
        check_enter_info = json.loads(check_enter_info.text)
        if check_enter_info["player1"] is not None and check_enter_info["player2"] is not None:
            self.pre_e = 1
        else:
            self.pre_e = 0

    def _self_opponent_hidden_check(self):
        check_hidden_url  = HIDDEN_URL
        headers = {"Content-Type":"application/json"}
        secret_data1 ={
            "player_id": USER1_ID,
            "hidden_number":  self.secret
        }
        # check_hidden_info = session.get(check_hidden_url)
        check_hidden_info = session.post(check_hidden_url, headers=headers, json=secret_data1)
        # print(check_hidden_info.text)
        if check_hidden_info.status_code == 400:
            if check_hidden_info.json()['detail'] == 'you can not select hidden':
                self.pre_h = 1
            else:
                self.pre_h = 0
        elif check_hidden_info.status_code == 200:
            check_hidden_info = json.loads(check_hidden_info.text)    
            if check_hidden_info["selecting"] == 'True' or check_hidden_info["selecting"] == 'False':
                self.pre_h = 1
            else:
                print("33")

    def _self_opponent_guess_check(self):
        headers = {"Content-Type":"application/json"}
        check_guess_url = GUESS_URL
        guess_data1 ={
            "player_id": USER1_ID,
            "guess": self.guess #args.ans
        }
        check_guess_info1 = session.post(check_guess_url,headers=headers,json=guess_data1)
        check_guess_info2 = json.loads(check_guess_info1.text)
        if check_guess_info1.status_code == 400 and check_guess_info1.json()["detail"] == 'opponent turn':
                self.pre_E = -1
            
        elif check_guess_info1.status_code == 200 and check_guess_info2["now_player"] != 'E':
                self.pre_E = 1
        else:
            print("E")


    def _winner(self) ->None:
        his_url = HISTORY_URL
        his_info = session.get(his_url)
        if his_info.json()['winner'] is not None:
            return 1
        else:
            return 0


    def _pre_room(self,room_id:int = ROOM_ID) -> int:
        room_url = ROOM_URL
        room_info =session.get(room_url)
        if room_info.status_code == 200 or room_info.status_code == 400:
            order_of_player = json.loads(room_info.text)
            if order_of_player['player1'] =='E':
                self.order = 1
                print("You are already in room {}, you are player1, your name is {}".format(room_id,order_of_player['player1']))
                # print(room_info.text)
            elif order_of_player['player2'] == 'E':
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
            "player_id": USER1_ID,
            "room_id": room_id
        }
        enter_room = session.post(enter_url,headers=headers,json=post_data1)
        enter_info = session.get(enter_url + '/' + str(room_id))
        # room_check = enter_info.json()
        room_check = json.loads(enter_info.text)
        print(room_check)
        if enter_room.status_code == 200 or enter_room.status_code == 400:
            if room_check['state'] == 1 and room_check['player1'] == 'E':
                self.wait = 1
                print("You are sucessfully entered room {},you are player1, please wait for another player".format(room_id))
                
            elif room_check['state'] == 1 and room_check['player2'] == 'E':
                self.wait = 1
                print("You are sucessfully entered room {},you are player2, please wait for another player".format(room_id))
                
            elif room_check['state'] == 2 and room_check['player1'] == 'E':
                self.wait = 2
                print("You are sucessfully entered room {},you are player1, game will start soon".format(room_id))
                
            elif room_check['state'] == 2 and room_check['player2'] == 'E':
                self.wait =2
                print("You are sucessfully entered room {},you are player2, game will start soon".format(room_id))
                
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
            "player_id": USER1_ID,
            "hidden_number": self.secret #args.ans
        }
        hidden_post = session.post(hidden_url,headers=headers,json=secret_data1)
        # print(hidden_post.text)
        # hidden_gene_info = hidden_post.json()
        hidden_gene_info = json.loads(hidden_post.text)
        if hidden_post.status_code == 200 :
            if hidden_gene_info['selecting'] == 'True':
                self.hid = 1
                print("Room {} :Secret generated, you are player1, please wait for opponent secret generation".format(ROOM_ID))
                
            elif hidden_gene_info['selecting'] == 'False':
                self.hid = 2
                print("Room {} :Secret generated, you are player2, now player1 will guess first".format(ROOM_ID))
                
            else:
                self.hid = -1
                print("Failed generate secret, please try again")
        elif  hidden_post.status_code == 400:
            if hidden_gene_info['detail'] == 'you can not select hidden':
                self.hid = 1
                print("Room {} :Secret already generated.".format(ROOM_ID))
                
            else:
                print("Error in hidden response")
        else:
            self.hid = -2
            print("Generate hidden number failed, please try again")
    

    def _get_HB(self):
    
    # HB=self.history() #[[1,[12345,1,0]],[2,[adf23,0,3]],[3,[...]]] 3次元配列
        hdx = len(self.history[1])
        H = self.history[1][hdx-1]
        print("getH: ",H)
        bdx = len(self.history[2])
        B = self.history[2][hdx-1]
        print("getB: ",B)
        self.tries=[-1][0]
        return([H,B])
# get_HB()

    def _HBidentify(self,answer,guess): #HBの計算
        self.hits = 0
        self.blows = 0
        for i in guess:
            if i in answer:
                if(guess.index(i) == answer.index(i)):
                    self.hits += 1
                else:
                    self.blows += 1
        return [self.hits,self.blows]

    def _get_random(self): #ランダムで桁数の数字を出力
        guess = ['0','1','2','3','4','5','6','7','8','9','a','b','c','d','e','f']#16進数の場合
        #guess = ['0','1','2','3','4','5','6','7','8','9']#10進数の場合
        random.shuffle(guess)
        self.guess = guess[:self.digits]
        return self.guess

    def _gen_answer(self):#正解のリストを生成
        self.ans = self._get_random()
        print("answer: ",self.ans)
        return self.ans

    def _detect_algorithm(self):#実際のアルゴリズム
        # self.tries=0
        while(True):
            self.tries += 1
            print(self.tries)
            #print("tries: ",tries)
            self.done = []
            while(len(self.done) != self.total_possibilities):
                while(True):
                    self.guess=self._get_random()
                    if(self.guess not in self.done):
                        self.done.append(self.guess)
                        break
                if(self.tries>1):
                    for j in range(self.tries-1):
                        h,b = self._HBidentify(self.guess,self.guessed_numbers[j])
                        if(h != self.hits[j] or b != self.blows[j]):#もう同じ組み合わせがあるかどうか
                            break
                    else:
                        self.guessed_numbers.append(self.guess)
                        break
                else:#chance=0
                    self.guessed_numbers.append(self.guess)
                    break
            else:
                print("error")
                break
            print("checked",len(self.done))
            print("guess: ",self.guess)
            
            while(True):
                #h,b=HBidentify(ans,guess)
                h,b=self._get_HB()
                print(h,"H",b,"B")
                # print("Guessed numbers:",len(self.guessed_numbers))
                #h = (int(input("Hits: ")))
                #b = (int(input("Blows: ")))
                if(h + b <= self.digits):
                    self.hits.append(h)
                    self.blows.append(b)
                    print()
                    break
            
            if(h == self.digits):
                print("finnish",self.tries)
                break
            


    # def algorithm_main():#return値は[2,3,a,d,f]
    #     #ans=gen_answer()
    #     self.detect_algorithm()




    def _guess_gene(self) ->None:
        guess_url = GUESS_URL
        headers = {"Content-Type":"application/json"}
        # while self.hit_num <5:
        #guess = random.sample(numberchoice,5)
        self._detect_algorithm()
        guess_al = self.guessed_numbers[-1]
        self.guess = "".join(guess_al)
        guess_data1 ={
            "player_id": USER1_ID,
            "guess":  self.guess#args.ans
        }
        guess_post1 = session.post(guess_url,headers=headers,json=guess_data1)
        # guess_gene_info = guess_post1.json()
        guess_gene_info = json.loads(guess_post1.text)
        # print(guess_gene_info)
        if guess_post1.status_code == 200 and guess_gene_info['now_player'] != 'E':
                self.turn = -1
                # if guess_gene_info['guesses'][-1] == self.guess:
                self.history[0].append(self.guess)
                # else:
                #     print("Opponent turn2, please wait")
                
        elif guess_post1.status_code == 400 and guess_gene_info['detail'] == 'opponent turn':
                self.turn = 1
                print("Opponent turnE2, please wait")
                
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
            # if his_get['table'][-1]['guess'] == self.guess:
            self.stage +=1
            self.hit_num = his_get['table'][-1]['hit']
            self.blow_num = his_get['table'][-1]['blow']
            self.history[1].append(self.hit_num)
            print(self.history[1])
            self.history[2].append(self.blow_num)
            print(self.history[2])
            return self.stage, self.history
            # else:
            #     print("History unmatch, please try again")
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


