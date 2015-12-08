import re

class cached_property(object):
    # taken from werkzeug (BSD license, original author: Armin Ronacher)
    not_none = False
    # if `not_none` is set, `cached_property` won't accept `None` as valid
    # `func` return value but will stay and wait for some non-`None` value.

    def __new__(cls, *args, **kwargs):
        if not args:
            from functools import partial
            return partial(cls, *args, **kwargs)
        else:
            return super(cls, cls).__new__(cls)

    def __init__(self, func, name=None, doc=None, not_none=False):
        self.func = func
        self.__name__ = name or func.__name__
        self.__doc__ = doc or func.__doc__
        self.not_none = not_none

    def __get__(self, obj, type=None):
        if obj is None:
            return self
        value = self.func(obj)
        if not (self.not_none and value is None):
            setattr(obj, self.__name__, value)
        return value

class Signal(object):

    @property
    def value(self):
        raise NotImplementedError()

class ConstSignal(Signal):

    def __init__(self, val):
        self.val = val

    @property
    def value(self):
        return self.val

class WireSignal(Signal):

    def __init__(self, wire):
        self.wire = wire

    @cached_property
    def value(self):
        return self.wire.signal.value

class GateSignal(Signal):

    def __init__(self, gate):
        self.gate = gate

    @cached_property
    def value(self):
        return self.gate.value


class Wire(object):

    def __init__(self, id, signal):
        self.id = id
        self.signal = signal

    def __str__(self):
        return "<Wire {}: {}>".format(self.id, str(self.signal.value))

    def __repr__(self):
        return str(self)

class BinaryGate(object):
    def __init__(self, in1, in2):
        self.in1 = in1
        self.in2 = in2

    @cached_property
    def value(self):
        return self.op(self.in1.value, self.in2.value)

    def op(self, x, y):
        raise NotImplementedError()

class AndGate(BinaryGate):
    def op(self, x, y):
        return x & y

class OrGate(BinaryGate):
    def op(self, x, y):
        return x | y

class LShiftGate(BinaryGate):
    def op(self, x, y):
        return (x << y) & 0xffff

class RShiftGate(BinaryGate):
    def op(self, x, y):
        return (x >> y) & 0xffff

class NotGate(object):
    def __init__(self, in1):
        self.in1 = in1

    @property
    def value(self):
        return (~self.in1.value) & 0xffff


GATES = {
    'and': AndGate,
    'or': OrGate,
    'lshift': LShiftGate,
    'rshift': RShiftGate
}

def isint(x):
    try:
        int(x)
        return True
    except ValueError:
        return False

def parse_instruction(raw):
    # signal to wire
    match = re.match("([a-z]+|\d+) -> ([a-z]+)", raw)
    if match is not None:
        w1, w2 = match.groups()
        return "wire", [w1, w2]

    # unary gates
    match = re.match("NOT ([a-z]+|\d+) -> ([a-z]+)", raw)
    if match is not None:
        in1, out = match.groups()

        return "not", [in1, out]

    # binary gates
    match = re.match("([a-z]+|\d+) (AND|OR|LSHIFT|RSHIFT) ([a-z]+|\d+) -> ([a-z]+)", raw)
    if match is not None:
        in1, op, in2, out = match.groups()

        return op.lower(), [in1, in2, out]

def get_wire(wires, id):
    if id not in wires:
        wire = Wire(id, None)
        wires[id] = wire

    return wires[id]

def get_signal(wires, encoded):
    if isint(encoded):
        return ConstSignal(int(encoded))
    else:
        return WireSignal(get_wire(wires, encoded))

def assemble(instructions):

    wires = {}

    for op, args in map(parse_instruction, instructions):
        if op == "wire":
            signal = get_signal(wires, args[0])
            wire = get_wire(wires, args[1])

            if isinstance(signal, WireSignal):
                wires[args[1]] = signal.wire
            else:
                wire.signal = signal
        elif op == "not":
            signal = get_signal(wires, args[0])
            wire = get_wire(wires, args[1])

            wire.signal = GateSignal(NotGate(signal))
        else:
            signal1 = get_signal(wires, args[0])
            signal2 = get_signal(wires, args[1])
            wire = get_wire(wires, args[2])

            gate = GATES[op]
            wire.signal = GateSignal(gate(signal1, signal2))


    return wires


if __name__ == '__main__':
    import sys

    instructions = sys.stdin.readlines()

    wires = assemble(instructions)

    print("Wire a has {}".format(wires["a"].signal.value))

    instructions.append("16076 -> b")

    wires = assemble(instructions)

    print("Wire a now has {}".format(wires["a"].signal.value))


