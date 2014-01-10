import sys

class Errors(object):
    def __init__(self):
        self.num_errors = 0
        self.num_warnings = 0
    
    def error(self, loc, msg):
        msg = self.create_message(loc, msg)
        print >>sys.stderr, msg
        self.num_errors += 1
    
    def warn(self, loc, msg):
        msg = self.create_message(loc, 'Warning: ' + msg)
        print >>sys.stderr, msg
        self.num_warnings += 1
    
    def create_message(self, loc, msg):
        return '%s: %s' % (loc, msg)
