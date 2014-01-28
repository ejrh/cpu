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
        for x in target:
            self.visit(x, **kwargs)

    def visit_parts(self, target, **kwargs):
        try:
            parts = target.get_parts()
        except AttributeError:
            parts = []
        
        for part in parts:
            self.visit(part, **kwargs)
