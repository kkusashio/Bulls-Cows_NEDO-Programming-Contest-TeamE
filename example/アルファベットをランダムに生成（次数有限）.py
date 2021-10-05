import random
LetterSeq = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
AccurateAnswer = random.choice(LetterSeq)
TimeFlag = 0

while TimeFlag != 5:
    UserAnswer = input('アルファベットを入力してください')

    if UserAnswer == AccurateAnswer:
        print('正解です')
        break
    elif UserAnswer > AccurateAnswer:
        print('大きすぎです')
    else:
        print('小さすぎます')

    TimeFlag += 1

if TimeFlag == 5:
    print('GameOver')