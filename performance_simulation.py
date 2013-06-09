import random
from points_generator import *

random.seed()

def algo1(count):
    # generate prices
    price = []
    for t in range(count):
        price.append(random.randint(0, 20000))
    # algorithm simulation
    ll = []
    for i in range(4):
        ll.append(random.randint(0, 20000))
    while len(price) > 0:
        # evaluate the trend
        # if keep up/down, then remove middle points
        # if have turn points, just keep them
        mx = max(ll)
        mn = min(ll)
        v = random.sample(price, 1)
        # remove points which diff < amp
        price.remove(v[0])


def algo2(count):
    # init
    pts = gen_points(count)
    amp = 500
    us = umax = pts[0]
    ds = dmin = pts[0]
    result = list()
    # calculate diff, if >= amp, then save init point
    for pt in pts[1:]:
        if pt > umax:
            if pt - us >= amp and umax - us < amp:
                result.append(us)
                ds = dmin = pt
            if pt > ds:
                ds = dmin = pt
            umax = pt
        elif pt < dmin:
            if ds - pt >= amp and ds - dmin < amp:
                result.append(ds)
                us = umax = pt
            if pt < us:
                us = umax = pt
            dmin = pt
    # clean-up
    if umax - us >= amp:
        result.append(umax)
    elif ds - dmin:
        result.append(dmin)
