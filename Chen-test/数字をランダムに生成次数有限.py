from random import randint
n = randint(1,100)
left = 1
right = 100
count = 1

while count <=3:
    num = int(input('整数を入力してください'))
    if num > n:
        print('大きすぎです')
        right = num
    elif num < n:
        print ('小さすぎです')
        left = num
    else:
        print('正解です')
        break
    count += 1
else:
    print('GameOver')