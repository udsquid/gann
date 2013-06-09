import random

random.seed()

def algo1(count):
    price = []
    for t in range(count):
        price.append(random.randint(0, 20000))

    ll = []
    for i in range(4):
        ll.append(random.randint(0, 20000))
    while len(price) > 0:
        mx = max(ll)
        mn = min(ll)
        v = random.sample(price, 1)
        price.remove(v[0])
