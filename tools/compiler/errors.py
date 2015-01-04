import sys
from utils import expect

class Errors(object):
    def __init__(self, filename=None):
        if filename is None:
            filename = '<input>'
        self.filename = filename
        self.num_errors = 0
        self.num_warnings = 0
    
    @expect.input(str)
    def error(self, loc, msg):
        msg = self.create_message(loc, msg)
        print >>sys.stderr, msg
        self.num_errors += 1
    
    @expect.input(str)
    def warn(self, loc, msg):
        msg = self.create_message(loc, 'Warning: ' + msg)
        print >>sys.stderr, msg
        self.num_warnings += 1
    
    @expect.input(str)
    def create_message(self, loc, msg):
        if loc == 'unknown':
            line, col = loc, loc
        else:
            line, col = loc
        return '%s:%s: %s' % (self.filename, line, msg)
