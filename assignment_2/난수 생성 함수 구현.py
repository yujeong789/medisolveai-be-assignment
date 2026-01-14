# 1번
# 숫자 1 혹은 0을 임의로 return 하는 get_1_or_0 함수를 구현하세요.
# function get_1_or_0() => int
import random

def get_1_or_0() -> int:
    return random.randint(0, 1)

# 2번
# 1.에서 작성한 get_1_or_0을 이용하여 숫자 n을 인자로 받아 0~n 사이의 임의의 정수를 반환하는 get_random 함수를 구현하세요.
# function get_random(int n) => int
def get_random(n: int) -> int:
    if n < 0:
        raise ValueError("n은 0 이상이어야 한다.")

    bits = n.bit_length()

    while True:
        value = 0
        for _ in range(bits):
            value = (value << 1) | get_1_or_0()

        if value <= n:
            return value

# for n in range(10):
#     print(get_random(n))

# 3번
# 2.에서 작성한 get_random 함수에 대한 테스트 함수를 최대한 넓은 범위를 cover할 수 있도록 작성하고, 구현 및 테스트 내역에 대한 보고서를 자유 형식으로 제출하세요.
# 해당 보고서는 과제 합격 시 발표자료로써 사용됩니다.
def test_edge_cases():
    assert get_random(0) == 0
    assert get_random(1) in (0, 1)
    print("✅ 경계값(0, 1) 테스트 통과")

def test_range(n: int, trials: int = 10000):
    for _ in range(trials):
        v = get_random(n)
        assert 0 <= v <= n
    print(f"✅ 범위(0 ~ {n}) 테스트 통과")

from collections import defaultdict

def test_distribution(n: int, trials: int = 100000):
    freq = defaultdict(int)

    for _ in range(trials):
        freq[get_random(n)] += 1

    print(f"\n📊 Distribution test (n={n})")
    for i in range(n + 1):
        print(f"{i}: {freq[i] / trials:.4f}")

if __name__ == "__main__":
    random.seed()

    test_edge_cases()
    test_range(10)
    test_range(100)
    test_range(1000)
    test_distribution(5)
