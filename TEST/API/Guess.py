#coding: UTF-8
import random
from typing import List,Tuple,Optional

numberchoice = ['0','1','2','3','4','5','6','7','8','9','a','b','c','d','e','f']

HIT_NUM = 0
BLOW_NUM = 0
MAX_STAGE = 5

class NumberGuess:
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
    def __init__(self, hit_num:int=0, blow_num:int=0, max_stage:int=5,ans: Optional[int] = None) -> None:
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
        
        self.g_history: List[int] = []
        self.h_history: List[int] = []
        self.b_history: List[int] = []
        self.history: Tuple[List[int],List[int],List[int]] = [self.g_history,self.h_history,self.b_history]
        # self.right = self.max_ans
        # self.left = self.min_ans

        if ans is not None:
            self.ans =ans
        else:
            self.ans = self._define_answer()
    
    def run(self,mode) ->Tuple[int,Tuple[List[int],List[int],List[int]]]:
        """数当てゲームを実行するランナー
        
        :param str mode: ゲームの実行モード("manual", "linear", "binary")
        :rtype: Tuple[int,List[int]]
        :return: 回答回数,回答履歴
        """
        if mode == "linear":
            self._play_game_auto_rand()
        # elif mode == "binary":
        #     self._play_game_auto_binary()
        else:
            self._play_game_manual()
        self._show_result()
        return self._get_history()

    def _get_your_guess(self) -> str:
        """手入力で遊ぶ時の入力文字をチェックする
        　数字でないものは受け付けず再入力とする
        
        :rtype: None
        :return: なし
        """
        while True:
            input_line=input('--推測した数字を入力してください-->> ')
            input_line = input_line.split()[0]
            input_str=input_line
            if len(input_str) == len(self.ans):
                guess_str=input_str
                print("--入力は{}".format(guess_str))
                return guess_str
            else:
                print("！！正しい桁数を入力してください！！")


    def _play_game_manual(self) :
        """手入力で遊ぶモード
        
        
        :rtype: None
        :return: なし
        """
        while self.stage < self.max_stage:
            print("--残り入力回数は{}".format(self.max_stage-self.stage))
            guess_str=self._get_your_guess()
            self.history[0].append(guess_str)
            self.history[1].append (self.hit_num)
            self.history[2].append(self.blow_num)
            print(self.stage)
            self.stage+=1
            print(self.stage)
            i=0
            j=0
            self.hit_num=0
            self.blow_num=0
            for i in range(len(self.ans)):
                if guess_str[i] == self.ans[i]:
                    self.hit_num+=1
                for j in range(len(self.ans)):
                    if(guess_str[i]==self.ans[j]):
                        self.blow_num+=1
            if self.hit_num == 5:
                break
            else:
                print(self.hit_num, self.blow_num-self.hit_num)

                # return self.hit_num, self.blow_num-self.hit_num


    def _play_game_auto_rand(self) -> None:
        """linearで遊ぶモード
        
        
        :rtype: None
        :return: なし
        """
        guess_str = random.sample(numberchoice,5)
        guess_str = "".join(numberchoice)
        while self.stage < self.max_stage:
            print("--残り入力回数は{}".format(self.max_stage-self.stage))
                
                
            self.history.append(guess_str)
            self.stage+=1
            for i in range(len(self.ans)):
                if guess_str[i] == self.ans[i]:
                    self.hit_num+=1
                for j in range(len(self.ans)):
                    if(guess_str[i]==self.ans[j]):
                        self.blow_num+=1         


    # def _play_game_auto_binary(self) -> None:
    #     """binaryで遊ぶモード
    #     :rtype: None
    #     :return: なし
    #     """
    #     while self.stage < self.max_stage:
    #         mid = self.left + ((self.right - self.left) // 2)
    #         num = mid
    #         print("--残り入力回数は{}".format(self.max_stage-self.stage))
    #         self.history.append(num)
    #         self.stage += 1
    #         if num > self.ans:
    #             print("!!もっと小さいよ!!")
    #             self.right = mid - 1
    #         elif num < self.ans:
    #             print("!!もっと大きいよ!!")
    #             self.left = mid + 1
    #         else:
    #             print("正解!")
    #             break

    def _show_result(self) -> None:
        """ゲーム結果を表示する
        回答入力の履歴と回答回数を示す
        
        
        :rtype: None
        :return: なし
        """
        if self.stage <= self.max_stage & self.hit_num ==5:    
            print("{}回で正解できました".format(self.stage))
        else:
            print("残念!!正解は{}でした。".format(self.ans))

        print('---------------')
        print("show history")
        for i,x in enumerate(self.history):
            print("{}回目：{}, hit: {}, blow, {}".format(i+1,self.history[0][i],self.history[1][i],self.history[2][i]))


    def _get_history(self) ->Tuple[int,Tuple[List[int],List[int],List[int]]]:
        """ゲーム結果を表示する
        回答入力の履歴と回答回数を示す
        
        
        :rtype: Tuple[int,List[int]]
        :return: 回答回数,回答履歴
        """
        return self.stage, self.history

    def _define_answer(self)-> str:
        """数当てゲームの答えを与える
        回答入力の履歴と回答回数を示す
        
        
        :rtype: int
        :return: 乱数で決めた数当ての答え
        """
        
        secret = random.sample(numberchoice,5)
        secret = "".join(secret)
        print(secret)
        return secret

    # def initialize_game(self) ->Tuple[int,int,List[int]]:
    #     ans=self.define_answer()
    #     stage =0
    #     history =[]
    #     return ans, stage, history      
