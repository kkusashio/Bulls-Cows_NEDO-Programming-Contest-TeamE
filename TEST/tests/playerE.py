#coding: UTF-8
"""
    *File name: test_mypj.py
    *Description:数当てゲームのmain関数をテストする
    *Created on: Oct 1st,2021
    *Created by: JIAHUI LIU
"""
import pytest
from TEST.API.game_pre import main
from TEST.API.game_pre import game_prepare
# from mypj import number_guess


def test_main() -> None:
    """
    main()関数のテスト
    分割統治法で解いた時の回数をチェックする
    """
    runner =game_prepare(hit_num=0,blow_num=0,max_stage=10,guess=12345)
    history = runner.run()

    # assert stage == 5