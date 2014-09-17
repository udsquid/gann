#
# 3-party libraries
#
from docopt import docopt, DocoptExit


#
# decorator definitions
#
def docopt_cmd(func):
    def fn(self, arg):
        try:
            option = docopt(func.__doc__, argv=arg)
        except DocoptExit as e:
            print "*** invalid command"
            print e
            return
        return func(self, option)

    fn.__name__ = func.__name__
    fn.__doc__ = func.__doc__
    return fn
