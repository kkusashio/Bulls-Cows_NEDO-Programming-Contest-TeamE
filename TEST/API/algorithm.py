import player1
import player2
import random
import math

digits=5 #桁数
numbers=10 #選択肢
tries = 0 #トライ数
hits = [] 
blows = []
guessed_numbers = [] #過去に予想したもの
total_possibilities = math.factorial(numbers)/math.factorial(numbers-digits) #可能性の総数
ans=[] #正解
guess=[] #そのトライでの予測

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
    #guess = ['0','1','2','3','4','5','6','7','8','9','a','b','c','d','e','f']
    guess = ['0','1','2','3','4','5','6','7','8','9']
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
        print("tries: ",tries)
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
            h,b=HBidentify(ans,guess)
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

ans=gen_answer()
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
