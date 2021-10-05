answer = [1, 2, 3, 4]
print(answer[0]) # 1
print(answer[1]) # 2

def hitblow(command, ans):
    hit = 0
    blow = 0
    for i in range(len(command)):
        if command[i] == ans[i]:
            hit += 1
        else:
            if command[i] in ans:
                blow += 1
    return [hit, blow]

import random
def generator(length):
    ans = []
    while len(ans) < length:
        rand = random.randint(0, 9)
        if rand in ans:
            pass
        else:
            ans += [rand]
    return ans

print("Hit & Blow Game")
digit = input("Please, enter the number of digits you want to play: ")
ans = generator(int(digit))
cont = True
count = 0
print("Game Start!")
while cont:
    count += 1
    command = input("enter the {} digits number > ".format(digit))
    your_ans = [int(command[i]) for i in range(len(command))]
    [hit, blow] = hitblow(your_ans, ans)
    print("{}: {} Hit, {} Blow".format(command, hit, blow))
    if hit == len(ans):
        print("Congratulations!!! You took {} steps.".format(count))
        cont = False

    your_ans = [int(command[i]) for i in range(len(command))]