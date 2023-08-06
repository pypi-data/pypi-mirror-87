from scipy.stats import beta
import matplotlib.pyplot as plt
import numpy as np
import sys


def _gen(alpha_, beta_, loc_=0, scale_=1):
    return np.linspace(
        beta.ppf(0.01, alpha_, beta_, loc_, scale_),
        beta.ppf(0.99, alpha_, beta_, loc_, scale_),
        100,
    )


def _plot(x, alpha_, beta_, loc_=0, scale_=1):
    plt.plot(
        x,
        beta.pdf(x, alpha_, beta_, loc=loc_, scale=scale_),
        label=f"Beta({alpha_}, {beta_})",
    )
    plt.show()


def main():
    abls = [1.0, 1.0, 0.0, 1.0]
    if len(sys.argv) == 1:
        exit("Usage: plot_beta alpha [beta [loc [scale]]]\n e.g. 2 8 10 50")
    for i in range(1, min(5, len(sys.argv))):
        abls[i - 1] = float(sys.argv[i])
    x = _gen(*abls)
    _plot(x, *abls)


if __name__ == "__main__":
    main()
