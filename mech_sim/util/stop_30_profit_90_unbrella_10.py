def long_cmd(open_price):
    upper = int(open_price) + 90 + 1
    lower = int(open_price) - 30
    umbrella = int(open_price) + 10
    print 'index searchf < {0} or >= {1}'.format(lower, upper)
    print 'index searchf < {0}'.format(umbrella)


def short_cmd(open_price):
    upper = int(open_price) + 30 + 1
    lower = int(open_price) - 90
    umbrella = int(open_price) - 10
    print 'index searchf >= {0} or < {1}'.format(upper, lower)
    print 'index searchf >= {0}'.format(umbrella)
