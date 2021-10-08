import random
import math

def count_BullsCows(answer,guess):
    hits = 0
    blows = 0
    for i in guess:
        if i in answer:
            if(guess.index(i) == answer.index(i)):
                hits += 1
            else:
                blows += 1
    return [hits,blows]

tries = 0
hits = [] 
blows = []
guessed_numbers = []
total_perms = math.factorial(16)/math.factorial(16-5)
#16*15*14*...*1
#総数

while(True):
    
    tries += 1
    print("tries: ",tries)
    
    done = []
    while(len(done) != total_perms):
        while(True):
            guess = ['0','1','2','3','4','5','6','7','8','9','a','b','c','d','e','f']
            random.shuffle(guess)
            guess = guess[:5]
            if(guess not in done):
                done.append(guess)
                break
        if(tries>1):
            for j in range(tries-1):
                h,b = count_BullsCows(guess,guessed_numbers[j])
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
        h = (int(input("Hits: ")))
        b = (int(input("Blows: ")))
        if(h + b <= 5):
            hits.append(h)
            blows.append(b)
            print()
            break
    
    if(h == 5):
        print("I won in %d chances" % tries)
        break