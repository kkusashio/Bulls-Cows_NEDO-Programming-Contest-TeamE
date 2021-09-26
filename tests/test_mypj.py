import pytest
from mypj.mypj import main, NumberGuess


def test_main() -> None:
    """
    main()関数のテスト
    分割統治法で解いた時の回数をチェックする
    """
    runner = NumberGuess(min_ans=0,max_ans=99,max_stage=10,ans=77)
    stage, history = runner.run("binary")

    assert stage == 1