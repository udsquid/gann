#!/usr/bin/env python

#
# project libraries
#
import high_low_reader as HLR


#
# constants
#
TIME_ERR = "The time of the %s item is wrong!"
PRICE_ERR = "The price of the %s item is wrong!"


#
# main procedure
#

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
# check the first record
t, p = first
print "Checking the first record.. ",
assert t == '1990/02/12', TIME_ERR % "first"
assert p == '12682', PRICE_ERR % "first"
print "OK"
# check middle one
print "Checking the middle record.. ",
t, p = middle
assert t == '1998/09/01', TIME_ERR % "middle"
assert p == '6219', PRICE_ERR % "middle"
print "OK"
# check the last one
print "Checking the last record.. ",
t, p = last
assert t == '2008/05/20', TIME_ERR % "last"
assert p == '9309', PRICE_ERR % "last"
print "OK"

# pass!
print "PASS!!"
