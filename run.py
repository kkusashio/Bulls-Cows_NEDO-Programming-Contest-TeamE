#coding: UTF-8
from mypj import number_guess
from mypj import mypj
def main() ->None:
    """数当てゲームのメイン
    :rtype:None
    :return: なし
    """
    args=mypj.get_parser()
    min_ans = int(args.min_ans)
    max_ans = int(args.max_ans)
    max_stage = int(args.max_stage)
    mode = args.mode
    

    # print(args.ans)
    if args.ans is not None:
        ans = int(args.ans)
        runner =number_guess.NumberGuess(min_ans=min_ans,max_ans=max_ans,max_stage=max_stage,ans=ans)
    else:
        runner = number_guess.NumberGuess(min_ans=min_ans,max_ans=max_ans,max_stage=max_stage)
    stage, history = runner.run(mode=mode)
    # ans, stage, history =initialize_game()
    # history, stage = play_game(stage, history,ans)
    # while stage < MAX_STAGE:
    #     print("残り入力回数は{}".format(MAX_STAGE-stage))
    #     num=get_your_guess()
    #     history.append(num)
    #     stage+=1
    #     if num>ans:
    #         print("もっと小さいよ")
    #     elif num<ans:
    #         print("もっと大きいよ")
    #     else:
    #         print("正解")
    #         break

    # show_result(stage,history)
    # if stage <= MAX_STAGE:
    #     print("{}回で正解できました".format(stage))
    # else:
    #     print("正解は{}でした。".format(ans))

    # print('---------------')
    # print("show history")
    # for i,x in enumerate(history):
    #     print("{}回目：{}".format(i+1,x))

if __name__ == '__main__':
    main()