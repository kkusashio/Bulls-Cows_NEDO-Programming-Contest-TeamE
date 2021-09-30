#https://qiita.com/gx3n-inue/items/396eddf69fbfa1eacc65
#https://www.tanaka.ecc.u-tokyo.ac.jp/ktanaka/papers/gpw96.pdf

#互いに異なるn桁のランダムな番号を返す(random.randint()版)
def create_random_n_digits_number(n:int) -> str:
    target_number_str = ""
    for _ in range(n):
        while True:
            d = str(random.randint(0, 9))
            if d not in target_number_str:
                target_number_str += d
                break
    return target_number_str

#互いに異なるn桁のランダムな番号を返す(random.sample()版)
def create_random_n_digits_number(n:int) -> str:
    return "".join([str(_) for _ in random.sample(list(range(10)), n)])

#質問の番号と解の候補の番号を照合し、Hit数とBlow数を返す（その１）
def response_check(n:int, answer_number:str, target_number:str) -> (int, int):
    """
    response check.
    """
    H, B = 0, 0
    for i in range(0, n):
        if target_number[i] == answer_number[i]:
            H += 1
        else:
            for j in range(0, n):
                if i != j and target_number[i] == answer_number[j]:
                    B += 1
    return H, B

#質問の番号と解の候補の番号を照合し、Hit数とBlow数を返す（その２）
def response_check(n:int, answer_number:str, target_number:str) -> (int, int):
    """
    response check.
    """
    H, B = 0, 0
    for n, m in zip(answer_number, target_number):
        if n == m:
            H += 1
        elif n in target_number:
            B += 1
    return H, B

#（初回の）解の候補となる番号のリストを作成する
def create_target_numbers(n:int)-> [str]:
    """
    create target numbers.
    """
    target_numbers = []

    def sub_create_target_numbers(n, workStr):
        if n == 0:
            target_numbers.append(workStr)
            return
        for i in range(10):
            if str(i) not in workStr:
                sub_create_target_numbers(n - 1, workStr + str(i))

    if n == 1:
        for i in range(10):
            target_numbers.append(str(i))

    elif n > 1:
        for i in range(10):
            sub_create_target_numbers(n - 1, str(i))

    return target_numbers

