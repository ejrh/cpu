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
        start_errors, start_warnings = (self.errors.num_errors, self.errors.num_warnings)
        self.log("Running %s" % self.name)
        try:
            return self.run_phase()
        except Exception, ex:
            self.log("Failed during %s with: %s" % (self.name, ex))
            raise
        finally:
            stop_time = time.time()
            self.log("Time spent on %s: %0.3f" % (self.name, stop_time - start_time))
            stop_errors, stop_warnings = (self.errors.num_errors, self.errors.num_warnings)
            if start_errors != stop_errors or start_warnings != stop_warnings:
                self.log("%d new errors and %d new warnings" % (stop_errors - start_errors, stop_warnings - start_warnings))

    def log(self, msg):
        print >>sys.stderr, msg
