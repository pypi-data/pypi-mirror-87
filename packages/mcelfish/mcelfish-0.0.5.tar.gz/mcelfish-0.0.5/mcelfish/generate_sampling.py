import random
import sys
import time


def _simulate(n, p):
    return len([1 for _ in range(n) if random.random() < p])


def main():
    p = 0
    sim = "--simulate" in sys.argv
    args = [e for e in sys.argv if e != "--simulate"]
    if len(args) > 1:
        N = int(args[1])
    else:
        N = random.randint(5, 250)
    print(f"N = {N}")

    if len(args) > 2:
        p = float(args[2])
    while not 0.01 < p < 0.99:
        p = round(random.random(), 2)
    print(f"p = {p}")

    current = N
    data = []
    while current > (N * 0.2) and len(data) < 35:
        if sim:
            q = _simulate(current, p)
        else:
            q = int(current * p)
        data.append(q)
        current -= q
    print(" ".join([str(e) for e in data]))


if __name__ == "__main__":
    main()
