#coding: UTF-8
"""
    *File name: test_mypj.py
    *Description:数当てゲームのmain関数をテストする
    *Created on: Oct 1st,2021
    *Created by: JIAHUI LIU
"""
import pytest
from mypj.mypj_t import main
from mypj.number_guess import NumberGuess
# from mypj import number_guess


def test_main() -> None:
    """
    main()関数のテスト
    分割統治法で解いた時の回数をチェックする
    """
    runner = NumberGuess(min_ans=0,max_ans=99,max_stage=10,ans=77)
    stage, history = runner.run("binary")

    assert stage == 5