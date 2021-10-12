# import player1
# import player2
import random
import math
from typing import List

class guess_algorithm:




    def __init__(self) -> None:
        """コンストラクタ
        :param int hit_ans:　一回hit数
        :param int blow_ans:　一回blow数
        :param int max_stage:　回答回数制限指定
        :rtype: None
        :return: なし
        """




        self.digits=5 #桁数
        self.numbers=16 #選択肢
        self.tries = 0 #トライ数
        self.numbers_of_tries=0
        self.hits = [] 
        self.blows = []
        self.guessed_numbers = [] #過去に予想したもの
        self.total_possibilities = math.factorial(self.numbers)/math.factorial(self.numbers-self.digits) #可能性の総数
        self.ans=[] #正解
        self.guess_al=[] #そのトライでの予測
        self.h_temp = 0
        self.b_temp = 0
        self.return_guess = 0 # 一回ランダムな数字を可能ナンバーに消して、実行できなくなると、また戻ります。
        self.temp_guess = []
        self.cross_guess = [] 
        self.and_guess = []
        # self.temp_ans = []
        self.done = []
        guess_array = ['0','1','2','3','4','5','6','7','8','9','a','b','c','d','e','f']#16進数の場合
        self.gu_re=guess_array

    def _HBidentify(self,answer,guess): #HBの計算
        hits = 0
        blows = 0
        for i in guess:
            if i in answer:
                if(guess.index(i) == answer.index(i)):
                    hits += 1
                else:
                    blows += 1
        return [hits,blows]

    def _get_random(self): #ランダムで桁数の数字を出力
        
        #guess = ['0','1','2','3','4','5','6','7','8','9']#10進数の場合
        random.shuffle(self.gu_re)
        self.guess_al = self.gu_re[:self.digits]
        return self.guess_al

    def _gen_answer(self):#正解のリストを生成
        ans_array = ['0','1','2','3','4','5','6','7','8','9','a','b','c','d','e','f']#16進数の場合
        self.ans = random.sample(ans_array,self.digits)
        print("answer: ",self.ans)
        return self.ans

    def _detect_algorithm(self):#実際のアルゴリズム
        self.tries=self.numbers_of_tries
        while(True):
            self.tries+=1
            print("tries: ",self.tries)
            nu_leave=len(self.gu_re)
            if nu_leave-self.digits>0:

                self.total_possibilities = math.factorial(nu_leave)/math.factorial(nu_leave-self.digits)
            else:
                self.total_possibilities = math.factorial(nu_leave)/math.factorial(self.digits)
            while(len(self.done) != self.total_possibilities):
                while(True):
                    self.guess_al=self._get_random()
                    if(self.guess_al not in self.done):
                        self.done.append(self.guess_al)
                        break
                if(self.tries>2):
                    for j in range(self.tries-1):
                        h,b = self._HBidentify(self.guess_al,self.guessed_numbers[j])
                        if(h != self.hits[j] or b != self.blows[j]):#もう同じ組み合わせがあるかどうか
                            break
                    else:
                        self.guessed_numbers.append(self.guess_al)
                        break
                else:#chance=0
                    self.guessed_numbers.append(self.guess_al)
                    break
            else:
                print("error")
                
            print("checked",len(self.done))
            print("guess: ",self.guess_al)
            while(True):
                h,b=self._HBidentify(self.ans,self.guess_al)
                print(h,"H",b,"B")
                #h = (int(input("Hits: ")))
                #b = (int(input("Blows: ")))
                if(h + b <= self.digits):
                    
                    
                    if h == 0 and b == 0:
                        if self.return_guess == 0:
                            self.return_guess = 0
                            self.gu_re = list(set(self.gu_re).difference(set(self.guess_al)))
                            
                        elif self.return_guess == 1:
                            self.return_guess = 0
                            self.gu_re = [i for i in self.gu_re if i not in self.temp_guess]
                            # self.gu_re = self.gu_re.remove(self.guess_al)
                            
                        else:
                            print("error happen in cross array calc of hb=0")

                    elif h + b <3:
                        if self.return_guess == 0:
                            # self.h_temp = h
                            # self.b_temp = b
                            self.return_guess = 1
                            self.temp_guess = self.guess_al
                            # self.gu_re = list(set(self.gu_re).difference(set(random.sample(self.temp_guess,h + b))))
                            
                        elif self.return_guess == 1:
                            if self.h_temp == h and self.b_temp == b:
                                self.gu_re = [x for x in self.gu_re if x not in set([i for i in self.temp_guess if i not in self.guess_al])] 
                            # self.h_temp = h
                            # self.b_temp = b
                            self.return_guess = 1
                            self.cross_guess = [x for x in self.temp_guess if x in set(self.guess_al)] 
                            self.and_guess = list(set(self.temp_guess).union(set(self.guess_al)))
                            self.temp_guess = self.guess_al
                            # self.gu_re = list(set(self.gu_re).difference(set(self.and_guess)))
                            num=random.randrange(h+b)
                            self.guess_al = list(set(random.sample(self.cross_guess,num)) | set(self.gu_re))
                            
                        elif self.return_guess == 2:
                            self.return_guess = 1
                            self.gu_re = list(set(self.gu_re) | set(self.temp_guess))
                            self.temp_guess = self.guess_al
                            
                        else:
                            print("error happened in hb<3")
                    elif h + b >=3 and h+b <5:
                        
                        if self.return_guess == 1:

                            self.return_guess = 2
                            self.h_temp = h
                            self.b_temp = b
                            self.temp_guess = self.guess_al
                            ans_f = random.sample(self.temp_guess,h+b)
                            
                            # self.gu_re = self.gu_re.remove(random.sample(self.temp_ans,self.digits-(h+b)))
                            self.guess_al = list(set(ans_f) | set(random.sample([i for i in self.gu_re if i not in self.temp_guess],self.digits-(h+b))))
                            
                        elif self.return_guess == 2:
                            self.return_guess = 2
                            self.h_temp = h
                            self.b_temp = b
                            nu_ll=len([i for i in self.gu_re if i not in self.temp_guess])
                            
                            # [self.digits-nu_ll,nu_ll][nu_ll>(self.digits-nu_ll)]
                            self.guess_al =list(set([i for i in self.gu_re if i not in self.temp_guess]) | set(random.sample(self.guess_al,self.digits-nu_ll)))
                            self.gu_re = list(set(self.gu_re) | set(self.guess_al))
                            self.temp_guess = self.guess_al
                            
                        else:
                            print("error in hb>3")
                    else:
                        print("aaa")
                    self.hits.append(h)
                    self.blows.append(b)
                    break
                

                if(h == self.digits):
                    print("finish",self.tries)
            


    # player1.game_prepare._get_history

    def _algorithm_main(self):#return値は[2,3,a,d,f]
    #ans=gen_answer()
        self.numbers_of_tries =0
        self._detect_algorithm()


run = guess_algorithm()
ans=run._gen_answer()
print(ans)
runner = run._algorithm_main()


'''
=possibilities=
---5---
5H
3H2B
2H3B
1H4B
5B
---4---
4H
3H1B
2H2B
1H3B
4B
---3---
3H
2H1B
1H2B
3B
---2---
2H
1H1B
2B
---1---
1H
1B
'''
