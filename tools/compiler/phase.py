import sys
import time

from compiler.errors import Errors

class Phase(object):
    def __init__(self, **kwargs):
        if 'name' in kwargs:
            self.name = kwargs['name']
        else:
            self.name = self.__class__.__name__

        if 'errors' in kwargs:
            self.errors = kwargs['errors']
        else:
            self.errors = Errors()
    
    def run(self):
        start_time = time.time()
        self.log("Running %s" % self.name)
        try:
            return self.run_phase()
        except Exception, ex:
            self.log("Failed during %s with: %s" % (self.name, ex))
            raise
        finally:
            stop_time = time.time()
            self.log("Time spent on %s: %0.3f" % (self.name, stop_time - start_time))

    def log(self, msg):
        print >>sys.stderr, msg
