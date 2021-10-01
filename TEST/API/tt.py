import random
from typing import List,Tuple,Optional
# numberchoice = ['0','1','2','3','4','5','6','7','8','9','a','b','c','d','e','f']
# gg = random.sample(numberchoice,5)
# input_line=input('--推測した数字を入力してください-->> ')
# input_line = input_line.split()[0]
# print(gg)
# gg = "".join(gg)
# print(gg)
# print(gg[0])
# print(input_line)
# print(len(input_line))
# print(len(gg))

ro0:list[int]=[]
ro1:list[int]=[]
ro2:list[int]=[]
ro:tuple[List[int],List[int],List[int]] = [ro0,ro1,ro2]
ro[0].append(1)
ro[1].append (2)
ro[2].append(3)
ro[0].append(2)
ro[1].append (4)
ro[2].append("s")
for i,x in enumerate(ro):
            print("{}回目：{}, hit: {}, blow, {}".format(i+1,ro[0][i],ro[1][i],ro[2][i]))