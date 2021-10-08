
#first question
f_q = ['0','1','2','3']
#chosen from
chosen_from = ['0','1','2','3','4','5','6','7','8','9','a','b','c','d','e','f','0','1','2','3']
#B=[]
#H=[]
H=[0,0,2,0,0,0,1,1,0,0,0,0,0]
B=[1,2,2,2,2,1,2,2,1,1,0,0,0]
answer_choice=[]
answer=[]
for i in range(16):
    if(B[0]+1==B[i]):
        pass
        

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
