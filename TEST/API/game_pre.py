# add additional functions
#coding: UTF-8
from typing import List,Tuple,Optional
import json
import random
import requests
from datetime import datetime
import time

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
ROOM_ID = 5005
ROOM_URL = URL + "/rooms/" + str(ROOM_ID)
ENTER_URL = URL + "/rooms"
HIDDEN_URL = ROOM_URL + "/players/" + USER1_NAME + "/hidden"
HISTORY_URL = ROOM_URL + "/players/" + USER1_NAME + "/table"
GUESS_URL = HIDDEN_URL + "/guesses"
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
        self.hid = 0
        self.turn = 0
        
        self.g_history: List[int] = []
        self.h_history: List[int] = []
        self.b_history: List[int] = []
        self.history: Tuple[List[int],List[int],List[int]] = [self.g_history,self.h_history,self.b_history]
        # self.right = self.max_ans
        # self.left = self.min_ans

        # if guess is not None:
        #     self.guess =guess
        # else:
        #     self.guess = self._define_answer()

    def run(self) ->Tuple[List[int],List[int],List[int]]:
        self._play_game_auto()
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
    
    def _play_game_auto(self)->None:
            self._pre_room()
            if self.order == 1:
                self._enter_room()
                if self.wait == 1:
                    timer(5)
                    self._enter_room()
                elif self.wait == 2:
                    self._hidden_gene()
                    if self.hid == 1:
                        timer(5)
                        self._hidden_gene()
                    elif self.hid == 2:
                        self._guess_gene()
                        if self.turn == 1:
                            self._get_history()
                        else:
                            timer(5)
                            self._guess_gene()
                    else:
                        print("error in guess input")
                else:
                    print("error in hidden number generation")
            else:
                print("error in entering room")
        


    # def _get_your_guess(self) -> str:
    #     """手入力で遊ぶ時の入力文字をチェックする
    #     　数字でないものは受け付けず再入力とする
        
    #     :rtype: None
    #     :return: なし
    #     """
    #     while True:
    #         input_line=input('--推測した数字を入力してください-->> ')
    #         input_line = input_line.split()[0]
    #         input_str=input_line
    #         if len(input_str) == len(self.ans):
    #             guess_str=input_str
    #             print("--入力は{}".format(guess_str))
    #             return guess_str
    #         else:
    #             print("！！正しい桁数を入力してください！！")
    

    # def _play_game_manual(self) :
    #     """手入力で遊ぶモード
        
        
    #     :rtype: None
    #     :return: なし
    #     """
    #     while self.stage < self.max_stage:
    #         print("--残り入力回数は{}".format(self.max_stage-self.stage))
    #         guess_str=self._get_your_guess()
    #         self.history[0].append(guess_str)
    #         self.history[1].append (self.hit_num)
    #         self.history[2].append(self.blow_num)
    #         print(self.stage)
    #         self.stage+=1
    #         print(self.stage)
    #         i=0
    #         j=0
    #         self.hit_num=0
    #         self.blow_num=0
    #         for i in range(len(self.ans)):
    #             if guess_str[i] == self.ans[i]:
    #                 self.hit_num+=1
    #             for j in range(len(self.ans)):
    #                 if(guess_str[i]==self.ans[j]):
    #                     self.blow_num+=1
    #         if self.hit_num == 5:
    #             break
    #         else:
    #             print(self.hit_num, self.blow_num-self.hit_num)

    #             # return self.hit_num, self.blow_num-self.hit_num
    


    # def _show_result(self) -> None:
    #     """ゲーム結果を表示する
    #     回答入力の履歴と回答回数を示す
        
        
    #     :rtype: None
    #     :return: なし
    #     """
    #     if self.stage <= self.max_stage & self.hit_num ==5:    
    #         print("{}回で正解できました".format(self.stage))
    #     else:
    #         print("残念!!正解は{}でした。".format(self.ans))

    #     print('---------------')
    #     print("show history")
    #     for i,x in enumerate(self.history):
    #         print("{}回目：{}, hit: {}, blow, {}".format(i+1,self.history[0][i],self.history[1][i],self.history[2][i]))


    # def _get_history(self) ->Tuple[int,Tuple[List[int],List[int],List[int]]]:
    #     """ゲーム結果を表示する
    #     回答入力の履歴と回答回数を示す
        
        
    #     :rtype: Tuple[int,List[int]]
    #     :return: 回答回数,回答履歴
    #     """
    #     return self.stage, self.history

    # def _define_answer(self)-> str:
    #     """数当てゲームの答えを与える
    #     回答入力の履歴と回答回数を示す
        
        
    #     :rtype: int
    #     :return: 乱数で決めた数当ての答え
    #     """
        
    #     secret = random.sample(numberchoice,5)
    #     secret = "".join(secret)
    #     print(secret)
    #     return secret

    def _pre_room(self,room_id:int = ROOM_ID) -> int:
        room_url = ROOM_URL
        room_info =session.get(room_url)
        if room_info.status_code == 200 or room_info.status_code == 400:
            order_of_player = json.loads(room_info.text)
            if order_of_player['player1'] =='E':
                self.order = 1
                print("You are already in room {}, you are player1, your name is {}".format(room_id,order_of_player['player1']))
                print(room_info.text)
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
        room_check = json.loads(enter_info.text)
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
                print("You are sucessfully entered room {},you are player1, game will start soon".format(room_id))
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
        secret = "".join(secret)
        secret_data1 ={
            "player_id": USER1_NAME,
            "hidden_number": secret #args.ans
        }
        hidden_post = session.post(hidden_url,headers=headers,json=secret_data1)
        print(hidden_post.text)
        hidden_gene_info = json.loads(hidden_post.text)
        if hidden_post.status_code == 200:
            if hidden_gene_info['selecting'] == 'True':
                self.hid = 1
                print("Room {} :Secret generated, you are player1, please wait for opponent secret generation".format(ROOM_ID))
            elif hidden_gene_info['selecting'] == 'False':
                self.hid = 2
                print("Room {} :Secret generated, you are player2, game will start soon".format(ROOM_ID))
            else:
                self.hid = -1
                print("Failed generate secret, please try again")
        # elif 
        else:
            self.hid = -2
            print("Generate hidden number failed, please try again")
    

    def _guess_gene(self) ->None:
        guess_url = GUESS_URL
        headers = {"Content-Type":"application/json"}
        guess = random.sample(numberchoice,5)
        self.guess = "".join(guess)
        guess_data1 ={
            "player_id": USER1_ID,
            "guess": guess #args.ans
        }
        guess_post1 = session.post(guess_url,headers=headers,json=guess_data1)
        guess_gene_info = json.loads(guess_post1.text)
        if guess_post1.status_code == 200:
            if guess_gene_info['now_player'] == 'E':
                self.turn = -1
                print("Opponent turn, please wait")
            else:
                self.turn = 1
                if guess_gene_info['guess'][-1] == self.guess:
                    self.history[0].append(guess)
                else:
                    print("Failed generate guess, please try again")
        else:
            print("Generate guess failed, please try again")


    def _get_history(self) -> Tuple[int,Tuple[List[int],List[int],List[int]]]: 
        his_url = HISTORY_URL
        his_info = session.get(his_url)
        his_get = json.loads(his_info.text)
        if his_info.status_code == 200:
            print(his_info.json())
            if his_info['winner'] is not None:
                if his_info['table'][-1]['guess'] == self.guess:
                    self.stage +=1
                    self.hit_num = his_get['table'][-1]['hit']
                    self.blow_num = his_get['table'][-1]['blow']
                    self.history[1].append(self.hit_num)
                    self.history[2].append(self.blow_num)
                    return self.stage, self.history
                else:
                    print("History unmatch, please try again")
            else:
                print("Winner has be generated, Congratulations!!{}!!, you will for {} times game".format(his_info['winner'],his_info['game_end_count']))
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


def timer(n):
    while True:
        print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        time.sleep(n)

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


