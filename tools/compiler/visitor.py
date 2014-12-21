class Visitor(object):
    def visit(self, target, **kwargs):
        cls = target.__class__
        while cls is not None:
            cls_name = cls.__name__
            try:
                visit_method = getattr(self, 'visit_' + cls_name)
                break
            except AttributeError:
                cls = cls.__base__
        if cls is None:
            visit_method = self.visit_parts
        
        return visit_method(target, **kwargs)
    
    def visit_list(self, target, **kwargs):
        rv = None
        for x in target:
            rv = self.visit(x, **kwargs)
        return rv

    def visit_parts(self, target, **kwargs):
        try:
            parts = target.get_parts()
        except AttributeError:
            parts = []
        
        rv = None
        for part in parts:
            rv = self.visit(part, **kwargs)
        return rv
