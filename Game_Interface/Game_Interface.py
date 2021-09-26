"""
To Do list
後にゲーム性を高める
CUIのみで良い→余力があればGUI

"""
import random

number = []
numberchoice = ['0','1','2','3','4','5','6','7','8','9','a','b','c','d','e','f']
attempts = 0

def GenerateNum():
    for i in range(5):
        x = random.randrange(0,16-i) # select random number between 0~16
        y = numberchoice[x]
        del numberchoice[x] #delete number used to prevent overlap
        number.append(y) # add elements to the list
    #print(number)

def TestFunc():
    print ("Answer is", number)

def GameEnd():
    print("GAME WON", " Attempts: ", attempts)

def Game():
    global attempts
    attempts+=1
    blow=0
    hit=0
    choice = input("0~fを5桁入力してください： ")
    guess = []
    for i in range(5):
        guess.append(choice[i])
    for i in range(5):
        if guess[i] == number[i]:
            hit+=1
        for j in range(5):
            if(guess[i]==number[j]):
                blow+=1
    
    #check if game won
    if(hit==5):
        GameEnd()
    
    #print result
    else:
        print("推測: ",choice,", HIT: ", blow, ", BLOW: ",hit," , attempts: ", attempts)

#Functions
GenerateNum()
TestFunc()
Game()

