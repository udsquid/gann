###
### project libraries
###
import high_low_reader as HLR


###
### constants
###
TIME_ERR = "The time of the %s item is wrong!"
PRICE_ERR = "The price of the %s item is wrong!"


###
### main procedure
###
# read indexes
import os.path
records = HLR.do_read(os.path.abspath("data/taiex_high_low.txt"))

# locate the first, middle, and last item
lower = 0
upper = len(records) - 1
average = (lower + upper) / 2

first = records[lower]
middle = records[average]
last = records[upper]

# check them all
t, p = first
assert t == '1990/02/12', TIME_ERR % "first"
assert p == '12682', PRICE_ERR % "first"
t, p = middle
assert t == '1998/09/01', TIME_ERR % "middle"
assert p == '6219', PRICE_ERR % "middle"
t, p = last
assert t == '2008/05/20', TIME_ERR % "last"
assert p == '9309', PRICE_ERR % "last"

# pass!
print "PASS!!"
