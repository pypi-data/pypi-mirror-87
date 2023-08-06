import os
import random

def re_is_pr(left, right):
    return random.randint(left, right)

def re_un(left, right):
    return random.uniform(left, right)

def calculate(pr, zzt, checkpoint):
    out = []
    index = checkpoint["acc"]
    r = int(index) // 10 - 1

    if len(pr) == len(zzt):
        for i in range(len(pr)):
            is_pr = re_is_pr(0,r)
            if is_pr == 0:
                out.append(pr[i])
            else:
                out.append(zzt[i])
    else:
        is_len = re_is_pr(0,r)
        if is_len == 0:
            final_len = len(pr)
            for i in range(len(pr) - 1):
                if i < len(zzt) - 1:
                    is_pr = re_is_pr(0,r)
                    if is_pr == 0:
                        out.append(pr[i])
                    else:
                        out.append(zzt[i])
                else:
                    out.append(pr[i])
            out.append(pr[-1])
        else:
            final_len = len(zzt)
            for i in range(len(zzt) - 1):
                if i < len(pr) - 1:
                    is_pr = re_is_pr(0,r)
                    if is_pr == 0:
                        out.append(pr[i])
                    else:
                        out.append(zzt[i])
                else:
                    out.append(zzt[i])    
            out.append(zzt[-1])

    # print("\n", out, zzt)
    return out

def score(checkpoint):
    index = checkpoint["acc"]
    # print("{:.3f}".format(acc - round(re_un(8,13),4)))
    return index - 2

def process_gradient(a, left, right):
    return a - random.randint(left, right)
