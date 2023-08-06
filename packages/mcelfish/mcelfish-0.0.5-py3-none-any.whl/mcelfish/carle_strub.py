def _weighted_sum(data):
    return sum((len(data) - (1 + i)) * e for (i, e) in enumerate(data))


def _z_pre_estimate(data, hatN):
    t = sum(data)
    x = _weighted_sum(data)
    k = len(data)

    tellerA = hatN - t + 0.5
    tellerB = (k * hatN - x) ** k
    nevner = (k * hatN - x - t) ** k

    return (tellerA * tellerB) / nevner - 0.5


def _cs_Eq(t, hatN, k, x):
    prod = 1
    for i in range(k):
        j = i + 1
        teller = k * hatN - x - t + 1 + k - j
        nevner = k * hatN - x + 2 + k - j
        prod *= (teller * 1.0) / nevner

    return t - 1 + ((hatN + 1) * prod)


def removal_carle_strub(data):
    t = sum(data)
    x = _weighted_sum(data)
    k = len(data)
    hatN = t

    for i in range(1000 * 1000):
        lhs = hatN + i
        rhs = _cs_Eq(t, lhs, k, x)
        if lhs >= rhs:
            return lhs
    raise ValueError("Unable to find CS solution")


assert removal_carle_strub([34, 46, 22, 26, 18, 16, 20, 12]) == 264


def removal_zippin(data):
    t = sum(data)
    k = len(data)
    x = _weighted_sum(data)
    z_min = ((t - 1) * (k - 1) / 2) - 1

    if x <= z_min:
        raise ValueError(f"Zippin X below z_min for {data}")

    hatN = t
    for i in range(1000 * 1000):
        lhs = hatN + i
        rhs = _z_pre_estimate(data, lhs)
        if rhs > lhs:
            return lhs

    raise ValueError("Unable to find CS solution")


assert removal_zippin([34, 46, 22, 26, 18, 16, 20, 12]) == 268


def main():
    from sys import argv

    if len(argv) < 2:
        exit("Usage: carle_strub 30 20 10 0")

    data = [int(e.lstrip(",").rstrip(",")) for e in argv[1:]]
    print("cs:", removal_carle_strub(data))
    print("z: ", removal_zippin(data))


if __name__ == "__main__":
    main()
