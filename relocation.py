from collections import deque
from contextlib import contextmanager
from mudeque import mudeque

class RelocationData(dict):
    pass

def context_get_relocation(context):
    relocation = context._buffer_stack[0]
    print "get_relocation: ", relocation, id(context._buffer_stack)
    if not isinstance(relocation, RelocationData):
        relocation = RelocationData()
        context._buffer_stack.insert(0, relocation)
    return relocation

@contextmanager
def branch(context, dest):
    print "BRANCHING"
    buffer = context._buffer_stack[-1]
    saved_deque = buffer.data
    buffer.data = context_get_relocation(context).setdefault(dest, deque())
    yield
    buffer.data = saved_deque

def destination(context, dest):
    print "DESTINATION"
    relocation = context_get_relocation(context)
    buffer = context._buffer_stack[-1]
    mdq = buffer.data = mudeque(buffer.data)
    # first branch off original stream
    mdq.branch()
    # then branch off destination leaving buffer.data at head
    new_mdq = mdq.branch(relocation.get(dest))
    print "relocation.get(%r): %r, mdq.branch(^^): %r" % (dest, relocation.get(dest), new_mdq)
    relocation[dest] = new_mdq
    print "mdq: %r relocation[%r]: %r" % (mdq, dest, relocation[dest])
