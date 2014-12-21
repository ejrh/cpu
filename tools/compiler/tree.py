class Tree(object):
    
    def __repr__(self):
        return self.__class__.__name__ + '(' + ', '.join(repr(x) for x in self.get_parts()) + ')'
    
    def __eq__(self, other):
        return self.__class__ == other.__class__ and self.get_parts() == other.get_parts()
    
    def __ne__(self, other):
        return not (self == other)

    def clone(self):
        cls = self.__class__
        cloned_parts = [clone(x) for x in self.get_parts()]
        try:
            return cls(*cloned_parts)
        except TypeError, ex:
            raise TypeError('Cannot clone %s using arguments %s' % (repr(cls), repr(cloned_parts)))


def clone(item):
    if isinstance(item, Tree):
        return item.clone()
    elif isinstance(item, list):
        return [clone(x) for x in item]
    else:
        return item
