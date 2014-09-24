#
# 3-party libraries
#
from docopt import docopt, DocoptExit


#
# decorator definitions
#
def docopt_cmd(group):
    def decorated(func):
        def wrapper(self, arg):
            try:
                option = docopt(group.__doc__, argv=arg)
            except DocoptExit as e:
                print "*** invalid command"
                print e
                return
            return func(self, option)

        wrapper.__name__ = func.__name__
        wrapper.__doc__ = group.__doc__
        return wrapper

    return decorated
