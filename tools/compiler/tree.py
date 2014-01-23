class Tree(object):
    
    def __repr__(self):
        return self.__class__.__name__ + '(' + ', '.join(repr(x) for x in self.get_parts()) + ')'
    
    def __eq__(self, other):
        return self.__class__ == other.__class__ and self.get_parts() == other.get_parts()
    
    def __ne__(self, other):
        return not (self == other)
