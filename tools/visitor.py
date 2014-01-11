class Visitor(object):
    def visit(self, target, **kwargs):
        cls_name = target.__class__.__name__
        try:
            visit_method = getattr(self, 'visit_' + cls_name)
        except AttributeError:
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
