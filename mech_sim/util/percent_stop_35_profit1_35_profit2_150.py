stop_loss = 35
profit_level_1 = 35
profit_level_2 = 150
profit_ratio_1 = 0.25
profit_ratio_2 = 0.75


def long_cmd(open_price, high_price=None, debug=False):
    if not high_price:
        high_price = open_price
    assert high_price >= open_price, \
        'highest price should be greater than or equal to open price'

    price_diff = high_price - open_price
    if price_diff >= profit_level_2 + 1:
        profit_range = int(round(price_diff * profit_ratio_2))
        close_price = open_price + profit_range
        instruction = 'index searchf < {0}'.format(close_price)
    elif price_diff >= profit_level_1 + 1:
        profit_range = int(round(price_diff * profit_ratio_1))
        close_price = open_price + profit_range
        instruction = 'index searchf < {0}'.format(close_price)
    else:
        upper = open_price + profit_level_1 + 1
        lower = open_price - stop_loss
        instruction = 'index searchf < {0} or >= {1}'.format(lower, upper)

    if debug:
        return instruction
    else:
        print instruction


def short_cmd(open_price, low_price=None, debug=False):
    if not low_price:
        low_price = open_price
    assert low_price <= open_price, \
        'lowest price should be less than or equal to open price'

    price_diff = open_price - low_price
    if price_diff > profit_level_2:
        profit_range = int(round(price_diff * profit_ratio_2))
        close_price = open_price - profit_range + 1
        instruction = 'index searchf >= {0}'.format(close_price)
    elif price_diff > profit_level_1:
        profit_range = int(round(price_diff * profit_ratio_1))
        close_price = open_price - profit_range + 1
        instruction = 'index searchf >= {0}'.format(close_price)
    else:
        upper = open_price + stop_loss + 1
        lower = open_price - profit_level_1
        instruction = 'index searchf >= {0} or < {1}'.format(upper, lower)

    if debug:
        return instruction
    else:
        print instruction


def test_long():
    print 'long_cmd(5000)'
    result = long_cmd(5000, debug=True)
    assert result == 'index searchf < 4965 or >= 5036', result

    print 'long_cmd(5000, 5035)'
    result = long_cmd(5000, 5035, debug=True)
    assert result == 'index searchf < 4965 or >= 5036', result

    print 'long_cmd(5000, 5035.99)'
    result = long_cmd(5000, 5035.99, debug=True)
    assert result == 'index searchf < 4965 or >= 5036', result

    print 'long_cmd(5000, 5036)'
    result = long_cmd(5000, 5036, debug=True)
    assert result == 'index searchf < 5009', result

    print 'long_cmd(5000, 5037)'
    result = long_cmd(5000, 5037, debug=True)
    assert result == 'index searchf < 5009', result

    print 'long_cmd(5000, 5150)'
    result = long_cmd(5000, 5150, debug=True)
    assert result == 'index searchf < 5038', result

    print 'long_cmd(5000, 5150.99)'
    result = long_cmd(5000, 5150.99, debug=True)
    assert result == 'index searchf < 5038', result

    print 'long_cmd(5000, 5151)'
    result = long_cmd(5000, 5151, debug=True)
    assert result == 'index searchf < 5113', result

    print 'long_cmd(5000, 5201)'
    result = long_cmd(5000, 5201, debug=True)
    assert result == 'index searchf < 5151', result

    print 'long_cmd(5000, 5300)'
    result = long_cmd(5000, 5300, debug=True)
    assert result == 'index searchf < 5225', result

    print 'PASS'


def test_short():
    print 'short_cmd(5000)'
    result = short_cmd(5000, debug=True)
    assert result == 'index searchf >= 5036 or < 4965', result

    print 'short_cmd(5000, 4965)'
    result = short_cmd(5000, 4965, debug=True)
    assert result == 'index searchf >= 5036 or < 4965', result

    print 'short_cmd(5000, 4964.99)'
    result = short_cmd(5000, 4964.99, debug=True)
    assert result == 'index searchf >= 4992', result

    print 'short_cmd(5000, 4963)'
    result = short_cmd(5000, 4963, debug=True)
    assert result == 'index searchf >= 4992', result

    print 'short_cmd(5000, 4960)'
    result = short_cmd(5000, 4960, debug=True)
    assert result == 'index searchf >= 4991', result

    print 'short_cmd(5000, 4850)'
    result = short_cmd(5000, 4850, debug=True)
    assert result == 'index searchf >= 4963', result

    print 'short_cmd(5000, 4849.99)'
    result = short_cmd(5000, 4849.99, debug=True)
    assert result == 'index searchf >= 4888', result

    print 'short_cmd(5000, 4849)'
    result = short_cmd(5000, 4849, debug=True)
    assert result == 'index searchf >= 4888', result

    print 'short_cmd(5000, 4848)'
    result = short_cmd(5000, 4848, debug=True)
    assert result == 'index searchf >= 4887', result

    print 'PASS'
