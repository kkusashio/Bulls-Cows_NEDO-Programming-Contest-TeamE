"""
done: get room
done: player_enter1
done: player_enter2(opponent)
done: hidden_post1→player2がいるかどうかを確認
done: hidden_post2(opponent)
done: guess_post1→相手がhidden postをしたかどうかを確認→仕様
    algorithm_player1.pyに最初のguessを出すように指示 algorithm_player1.guess()

done: guess_post2→(opponent)
"""

import player1
# from player1 import game_prepare #[[12aef,1,2],[54313,2,2],
import random
import math

digits=5 #桁数
numbers=16 #選択肢
tries = 0 #トライ数
hits = [] 
blows = []
guessed_numbers = [] #過去に予想したもの
total_possibilities = math.factorial(numbers)/math.factorial(numbers-digits) #可能性の総数
ans=[] #正解
guess=[] #そのトライでの予測

def get_HB():
    args = player1.get_parser()
    HB=args.hit_number #[[1,[12345,1,0]],[2,[adf23,0,3]],[3,[...]]] 3次元配列
    H=HB[-1][1][1]
    print("getH: ",H)
    B=HB[-1][1][2]
    print("getB: ",B)
    tries=[-1][0]
    return([H,B])
# get_HB()

def HBidentify(answer,guess): #HBの計算
    hits = 0
    blows = 0
    for i in guess:
        if i in answer:
            if(guess.index(i) == answer.index(i)):
                hits += 1
            else:
                blows += 1
    return [hits,blows]

def get_random(): #ランダムで桁数の数字を出力
    guess = ['0','1','2','3','4','5','6','7','8','9','a','b','c','d','e','f']#16進数の場合
    #guess = ['0','1','2','3','4','5','6','7','8','9']#10進数の場合
    random.shuffle(guess)
    guess = guess[:digits]
    return guess

def gen_answer():#正解のリストを生成
    ans = get_random()
    print("answer: ",ans)
    return ans

def detect_algorithm():#実際のアルゴリズム
    tries=0
    while(True):
        tries += 1
        #print("tries: ",tries)
        done = []
        while(len(done) != total_possibilities):
            while(True):
                guess=get_random()
                if(guess not in done):
                    done.append(guess)
                    break
            if(tries>1):
                for j in range(tries-1):
                    h,b = HBidentify(guess,guessed_numbers[j])
                    if(h != hits[j] or b != blows[j]):#もう同じ組み合わせがあるかどうか
                        break
                else:
                    guessed_numbers.append(guess)
                    break
            else:#chance=0
                guessed_numbers.append(guess)
                break
        else:
            print("error")
            break
        print("checked",len(done))
        print("guess: ",guess)
        
        while(True):
            #h,b=HBidentify(ans,guess)
            h,b=get_HB()
            print(h,"H",b,"B")
            #h = (int(input("Hits: ")))
            #b = (int(input("Blows: ")))
            if(h + b <= digits):
                hits.append(h)
                blows.append(b)
                print()
                break
        
        if(h == digits):
            print("finnish",tries)
            break
        return guess


def algorithm_main():#return値は[2,3,a,d,f]
    #ans=gen_answer()
    detect_algorithm()

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
