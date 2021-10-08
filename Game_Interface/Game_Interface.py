"""
To Do list
後にゲーム性を高める
CUIのみで良い→余力があればGUI

"""
import random

ans = []
numberchoice = ['0','1','2','3','4','5','6','7','8','9','a','b','c','d','e','f']
numberchoices = ['0','1','2','3','4','5','6','7','8','9','a','b','c','d','e','f']
attempts = 0
gamewon=False

def GenerateNum():
    for i in range(5):
        x = random.randrange(0,16-i) # select random number between 0~16
        y = numberchoice[x]
        del numberchoice[x] #delete number used to prevent overlap
        ans.append(y) # add elements to the list
    print(ans)

def Hit_Blow_detector(answer,guess):
    hits = 0
    blows = 0
    for i in guess:
        if i in answer:
            if(guess.index(i) == answer.index(i)):
                hits += 1
            else:
                blows += 1
    return [hits,blows]

def TestFunc():
    print ("Answer is", ans)

def GameEnd():
    print("GAME WON", " Attempts: ", attempts)

def get_unique_list(seq):
    seen = []
    return [x for x in seq if x not in seen and not seen.append(x)]

def Game():
    global attempts
    attempts+=1
    blow=0
    hit=0
    valid_num=False
    while (valid_num == False):
        valid_input_char=False
        invalid_input_len=False  
        invalid_input_same=False
        choice = input("0~fを5桁入力してください： ")
        if (len(choice)!=5):
            invalid_input_len=True
        for i in range(len(choice)):
            for j in range(len(numberchoices)):
                if choice[i]==numberchoices[j]:
                    valid_input_char=True
        if (len(choice)!=len(set(choice))):
            invalid_input_same=True
        if valid_input_char==False:
            print("Invalid character, try again")
        if invalid_input_len==True:
            print("Invalid digits, try again")  
        if invalid_input_same==True:
            print("Same character cannot be used twice, try again")   
        else:
            valid_num=True
    guess = []
    for i in range(5):
        guess.append(choice[i])
    for i in range(5):
        if guess[i] == ans[i]:
            hit+=1
        for j in range(5):
            if(guess[i]==ans[j]):
                blow+=1
    
    #check if game won
    if(hit==5):
        gamewon=True
        GameEnd()
    
    #print result
    else:
        print("推測: ",choice,", HIT: ", blow, ", BLOW: ",hit," , attempts: ", attempts)

#Functions
GenerateNum()
TestFunc()
while gamewon==False:
    Game()

