#import player1 #[[12aef,1,2],[54313,2,2],
#import player2
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
"""
def get_HB():
    HB=player1.game_prepare._get_history #[[1,[12345,1,0]],[2,[adf23,0,3]],[3,[...]]] 3次元配列
    H=HB[-1][1][1]
    print("getH: ",H)
    B=HB[-1][1][2]
    print("getB: ",B)
    tries=[-1][0]
    return([H,B])
"""

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
            h,b=HBidentify(ans,guess)
            #print(h,"H",b,"B")
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

gen_answer()
detect_algorithm()