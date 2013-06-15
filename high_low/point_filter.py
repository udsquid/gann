###
### module variable
###
amp = 0
us = umax = None
ds = dmin = None
result = None


###
### module methods
###
def init(amplitude):
    """Initialize the filter state."""
    global amp, us, umax, ds, dmin, result
    amp = amplitude
    # reset pointers and result
    us = umax = None
    ds = dmin = None
    result = list()


def forward(point):
    """Forward a point and update related peak/trough pointers."""
    global amp, us, umax, ds, dmin, result
    t = point.time.strftime("%Y-%m-%d")
    p = point.price
    if not all([us, umax, ds, dmin]):
        us = umax = p
        ds = dmin = p
    if p > umax:
        # if new_high - up_start >= amplitude, save up_start as peak
        if p - us >= amp and umax - us < amp:
            result.append(dict(price=us))
            ds = dmin = p
        # need to reset down pointers?
        if p > ds:
            ds = dmin = p
        # update up_max
        umax = p
    elif p < dmin:
        # if down_start - new_low >= amplitude, save down_start as trough
        if ds - p >= amp and ds - dmin < amp:
            result.append(dict(price=ds))
            us = umax = p
        # need to reset up pointers?
        if p < us:
            us = umax = p
        # update down_min
        dmin = p


def forward2(point):
    """Forward a point and update related peak/trough pointers."""
    global amp, us, umax, ds, dmin, result
    pt = dict(time=str(point.time), price=point.price)
    if not all([us, umax, ds, dmin]):
        us = umax = pt
        ds = dmin = pt
    if pt['price'] > umax['price']:
        # if new_high - up_start >= amplitude, save up_start as peak
        if pt['price'] - us['price'] >= amp and \
           umax['price'] - us['price'] < amp:
            result.append(us)
            ds = dmin = pt
        # need to reset down pointers?
        if pt['price'] > ds['price']:
            ds = dmin = pt
        # update up_max
        umax = pt
    elif pt['price'] < dmin['price']:
        # if down_start - new_low >= amplitude, save down_start as trough
        if ds['price'] - pt['price'] >= amp and \
           ds['price'] - dmin['price'] < amp:
            result.append(ds)
            us = umax = pt
        # need to reset up pointers?
        if pt['price'] < us['price']:
            us = umax = pt
        # update down_min
        dmin = pt


def cleanup():
    """Finalize the filter."""
    global amp, us, umax, ds, dmin, result
    if umax - us >= amp:
        result.append(dict(price=umax))
    elif ds - dmin >= amp:
        result.append(dict(price=dmin))


def cleanup2():
    """Finalize the filter."""
    global amp, us, umax, ds, dmin, result
    if umax['price'] - us['price'] >= amp:
        result.append(umax)
    elif ds['price'] - dmin['price'] >= amp:
        result.append(dmin)


def get_result():
    """Get the list of peak/trough points."""
    global result
    return result
