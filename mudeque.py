from copy import copy
from collections import deque
from itertools import chain

def get_proxy_func(name, dest):
    def first(self, *args, **kwargs):
        return getattr(self.deques[0], name)(*args, **kwargs)
    def last(self, *args, **kwargs):
        return getattr(self.deques[-1], name)(*args, **kwargs)
    def all(self, *args, **kwargs):
        list(getattr(dq, name)(*args, **kwargs) for dq in self.deques)
    def sum(self, *args, **kwargs):
        return sum(getattr(dq, name)(*args, **kwargs) for dq in self.deques)
    def unimplemented(self, *args, **kwargs):
        raise NotImplementedError()
    wrapper = locals()[dest]
    wrapper.__name__ = name
    wrapper.func_name = name
    return wrapper

class mudeque(object):
    def __init__(self, original=None, cls=deque):
        self.deques = [original or cls()]
        self.cls = cls

    def __copy__(self):
        ret = self.__class__()
        ret.deques = self.deques[:]
        ret.cls = self.cls
        return ret

    def branch(self, new_deque=None):
        orig_tail = copy(self)
        print "branch: ", self, orig_tail
        if new_deque is None:
            new_deque = self.cls()
        self.deques.append(new_deque)
        return orig_tail

    ## proxy methods
    for name, dest in dict(
                append='last', extend='last', pop='last',
                appendleft='first', extendleft='first', popleft='first',
                clear='all', __len__='sum',
                remove='unimplemented', rotate='unimplemented',
            ).iteritems():
        locals()[name] = get_proxy_func(name, dest)
    del name, dest

    def __iter__(self):
        print "Iterating on", self
        return chain(*self.deques)

    def __repr__(self):
        return 'mudeque(%s)'%(', '.join('[%s]'%(', '.join(repr(item) for item in dq)) for dq in self.deques))

