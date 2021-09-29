from random import randint
n = randint(1,100)
left = 1
right = 100
while True:
    num = int(input(f'整数を入力してください　({left}-{right}) :'))
    if num > n:
        print('大きすぎです')
        right = num
    elif num < n:
        print('小さすぎです')
        left = num
    else:
        print('正解です')