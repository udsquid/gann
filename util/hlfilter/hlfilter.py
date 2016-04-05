import click

@click.command()
@click.argument('amplitude', type=click.INT)
@click.argument('data', type=click.File('r'), default='-')
def cli(amplitude, data):
    """Filter high/low prices by given amplitude."""
    all_prices = get_prices(data)
    fit_prices = filter_prices(all_prices, amplitude)
    for price in fit_prices:
        click.echo(price)

def get_prices(source):
    prices = []
    while True:
        line = source.readline()
        line = line.strip()
        if not line:
            break
        if ' ' in line:
            raise click.ClickException('Should not contain space(s).')

        price = int(line)
        prices.append(price)

    return prices

def filter_prices(prices, amplitude):
    result = []
    if len(prices) < 2:         # must have at least 2 prices
        return result

    # there are two types of situations that will need to move
    # rise_start/rise_max and fall_start/fall_min:
    # 1. the first time diff >= amplitude
    # 2. rise_start/fall_start being broken
    rise_start = rise_max = prices[0]
    fall_start = fall_min = prices[0]
    for price in prices[1:]:
        if price > rise_max:
            old_diff = rise_max - rise_start
            new_diff = price - rise_start
            if old_diff < amplitude and new_diff >= amplitude:
                result.append(rise_start)
                fall_start = fall_min = price
            if price > fall_start:
                fall_start = fall_min = price
            rise_max = price
        elif price < fall_min:
            old_diff = fall_start - fall_min
            new_diff = fall_start - price
            if old_diff < amplitude and new_diff >= amplitude:
                result.append(fall_start)
                rise_start = rise_max = price
            if price < rise_start:
                rise_start = rise_max = price
            fall_min = price

    # save last point
    rise_diff = rise_max - rise_start
    if rise_diff >= amplitude:
        result.append(rise_max)
    fall_diff = fall_start - fall_min
    if fall_diff >= amplitude:
        result.append(fall_min)

    return result
