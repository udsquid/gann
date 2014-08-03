import random
import itertools

# init
random.seed()

# data
diff_range = range(18, 45)
diff_pool = [d*10 for d in diff_range]

sign = itertools.cycle([1, -1])

# helper functions
def get_avg_diffs(num=10):
    for t in range(random.randint(0, 1)):
        sign.next()
    return [n*sign.next() for n in random.sample(diff_pool, num)]


def get_real_diffs(num):
    p = diff_pool.index(200)
    diff_small = diff_pool[:p]
    diff_large = diff_pool[p:]
    # shuffle sign
    for t in range(random.randint(0, 1)):
        sign.next()
    # generate diffs
    wave = random.randint(4, 6)
    reverse = False
    res = list()
    for t in range(num):
        if reverse:
            if t % 2 == 0:
                diff = random.sample(diff_small, 1)
            else:
                diff = random.sample(diff_large, 1)
        else:
            if t % 2 == 0:
                diff = random.sample(diff_large, 1)
            else:
                diff = random.sample(diff_small, 1)
        # print diff[0]
        res.append(sign.next()*diff[0])
        if t % wave == wave-1:
            # print '-'*30
            reverse = not reverse
            wave = random.randint(4, 6)
    return res


def gen_points(num=10, init=5000, algo=1):
    cur = init
    res = list()
    if algo == 1:
        diff_list = get_real_diffs(num-1)
    elif algo == 2:
        diff_list = get_avg_diffs(num-1)

    for d in diff_list:
        cur = cur + d
        cur = max(cur, 0)
        res.append(cur)
    return [init] + res
