# coding:utf-8
import sys

import numpy as np


def adder(a, b):
    d = np.arange(12).reshape(3, 4)
    return a + b + d


if __name__ == '__main__':
    a = []
    for i in range(1, len(sys.argv)):
        a.append((int(sys.argv[i])))

    print(adder(a[0], a[1]))
