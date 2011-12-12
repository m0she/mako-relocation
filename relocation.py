from collections import deque
from contextlib import contextmanager
from mudeque import mudeque

class RelocationData(dict):
    pass

def context_get_relocation(context):
    relocation = context._buffer_stack[0]
    if not isinstance(relocation, RelocationData):
        relocation = RelocationData()
        context._buffer_stack.insert(0, relocation)
    return relocation

@contextmanager
def branch(context, dest):
    buffer = context._buffer_stack[-1]
    saved_deque = buffer.data
    buffer.data = context_get_relocation(context).setdefault(dest, deque())
    yield
    buffer.data = saved_deque

def destination(context, dest):
    relocation = context_get_relocation(context)
    buffer = context._buffer_stack[-1]
    mdq = buffer.data = mudeque(buffer.data)
    # first branch off original stream
    mdq.branch()
    # then branch off destination leaving buffer.data at head
    new_mdq = mdq.branch(relocation.get(dest))
    relocation[dest] = new_mdq
