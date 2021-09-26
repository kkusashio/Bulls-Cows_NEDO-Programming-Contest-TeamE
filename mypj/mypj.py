import random
import argparse
from typing import List,Tuple,Optional

MIN_ANS = 0
MAX_ANS = 9
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
    def __init__(self, min_ans:int=0, max_ans:int=9, max_stage:int=5,ans: Optional[int] = None) -> None:
        """コンストラクタ
        :param int min_ans:　出題範囲指定　下限
        :param int max_ans:　出題範囲指定　下限
        :param int max_stage:　回答回数制限指定
        :rtype: None
        :return: なし
        """
        self.min_ans = min_ans
        self.max_ans = max_ans
        self.max_stage = max_stage
        self.stage = 0
        self.history: List[int] = []
        self.right = self.max_ans
        self.left = self.min_ans

        if ans is not None:
            self.ans =ans
        else:
            self.ans = self._define_answer()
    
    def run(self,mode) ->Tuple[int,List[int]]:
        """数当てゲームを実行するランナー
        
        :param str mode: ゲームの実行モード("manual", "linear", "binary")
        :rtype: Tuple[int,List[int]]
        :return: 回答回数,回答履歴
        """
        if mode == "linear":
            self._play_game_auto_linear()
        elif mode == "binary":
            self._play_game_auto_binary()
        else:
            self._play_game_manual()
        self._show_result()
        return self._get_history()

    def _get_your_guess(self) -> int:
        """手入力で遊ぶ時の入力文字をチェックする
        　数字でないものは受け付けず再入力とする
        
        :rtype: None
        :return: なし
        """
        while True:
            input_line=input('--数字を入力してください-->> ')
            input_str=input_line.split()[0]
            if input_str.isdecimal():
                num=int(input_str)
                print("--入力は{}".format(num))
                return num
            else:
                print("！！数字ではありませんです！！")


    def _play_game_manual(self) -> None:
        """手入力で遊ぶモード
        
        
        :rtype: None
        :return: なし
        """
        while self.stage < self.max_stage:
            print("--残り入力回数は{}".format(self.max_stage-self.stage))
            num=self._get_your_guess()
            self.history.append(num)
            self.stage+=1
            if num>self.ans:
                print("!!もっと小さいよ!!")
            elif num<self.ans:
                print("!!もっと大きいよ!!")
            else:
                print("正解！")
                break

    def _play_game_auto_linear(self) -> None:
        """linearで遊ぶモード
        
        
        :rtype: None
        :return: なし
        """
        num =(self.min_ans + self.max_ans)//2
        while self.stage < self.max_stage:
            print("--残り入力回数は{}".format(self.max_stage-self.stage))
                
                
            self.history.append(num)
            self.stage+=1
            if num>self.ans:
                print("!!もっと小さいよ!!")
                num -=1
            elif num<self.ans:
                print("!!もっと大きいよ!!")
                num +=1
            else:
                print("正解!")
                break

    def _play_game_auto_binary(self) -> None:
        """binaryで遊ぶモード
        
        
        :rtype: None
        :return: なし
        """
        while self.stage < self.max_stage:
            mid = self.left + ((self.right - self.left) // 2)
            num = mid
            print("--残り入力回数は{}".format(self.max_stage-self.stage))
                
                
            self.history.append(num)
            self.stage += 1
            if num > self.ans:
                print("!!もっと小さいよ!!")
                self.right = mid - 1
            elif num < self.ans:
                print("!!もっと大きいよ!!")
                self.left = mid + 1
            else:
                print("正解!")
                break

    def _show_result(self) -> None:
        """ゲーム結果を表示する
        回答入力の履歴と回答回数を示す
        
        
        :rtype: None
        :return: なし
        """
        if self.stage <= self.max_stage:
            print("{}回で正解できました".format(self.stage))
        else:
            print("正解は{}でした。".format(self.ans))

        print('---------------')
        print("show history")
        for i,x in enumerate(self.history):
            print("{}回目：{}".format(i+1,x))


    def _get_history(self) ->Tuple[int,List[int]]:
        """ゲーム結果を表示する
        回答入力の履歴と回答回数を示す
        
        
        :rtype: Tuple[int,List[int]]
        :return: 回答回数,回答履歴
        """
        return self.stage, self.history

    def _define_answer(self)->int:
        """数当てゲームの答えを与える
        回答入力の履歴と回答回数を示す
        
        
        :rtype: int
        :return: 乱数で決めた数当ての答え
        """
        return random.randint(self.min_ans,self.max_ans)

    # def initialize_game(self) ->Tuple[int,int,List[int]]:
    #     ans=self.define_answer()
    #     stage =0
    #     history =[]
    #     return ans, stage, history      

def get_parser() ->argparse.Namespace:
    """コマンドライン引数を解析したものをもつ

    :rtype:argparse.Namespace
    :return: コマンド値
    """
    parser=argparse.ArgumentParser(description='数当てゲーム')
    parser.add_argument('--min_ans',default=0)
    parser.add_argument('--max_ans',  default=99)
    parser.add_argument('--max_stage', default=10)
    parser.add_argument("--ans")
    parser.add_argument('--mode', default="manual")
    args=parser.parse_args()
    return args

def main() ->None:
    """数当てゲームのメイン
    :rtype:None
    :return: なし
    """
    args=get_parser()
    min_ans = int(args.min_ans)
    max_ans = int(args.max_ans)
    max_stage = int(args.max_stage)
    mode = args.mode
    

    # print(args.ans)
    if args.ans is not None:
        ans = int(args.ans)
        runner = NumberGuess(min_ans=min_ans,max_ans=max_ans,max_stage=max_stage,ans=ans)
    else:
        runner = NumberGuess(min_ans=min_ans,max_ans=max_ans,max_stage=max_stage)
    stage, history = runner.run(mode=mode)
    # ans, stage, history =initialize_game()
    # history, stage = play_game(stage, history,ans)
    # while stage < MAX_STAGE:
    #     print("残り入力回数は{}".format(MAX_STAGE-stage))
    #     num=get_your_guess()
    #     history.append(num)
    #     stage+=1
    #     if num>ans:
    #         print("もっと小さいよ")
    #     elif num<ans:
    #         print("もっと大きいよ")
    #     else:
    #         print("正解")
    #         break

    # show_result(stage,history)
    # if stage <= MAX_STAGE:
    #     print("{}回で正解できました".format(stage))
    # else:
    #     print("正解は{}でした。".format(ans))

    # print('---------------')
    # print("show history")
    # for i,x in enumerate(history):
    #     print("{}回目：{}".format(i+1,x))
if __name__ == '__main__':
    main()