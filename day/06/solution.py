import re

class BaseGrid(object):

    def __init__(self, rows, cols, default=False):
        self.rows = rows
        self.cols = cols
        self.lights = [default] * (rows * cols)

    def on(self, x, y):
        raise NotImplementedError()

    def off(self, x, y):
        raise NotImplementedError()

    def toggle(self, x, y):
        raise NotImplementedError()

    def is_on(self, value):
        raise NotImplementedError()

    def count_on(self):
        return sum(filter(self.is_on, self.lights))

    def _index(self, x, y):
        return x * self.rows + y

class BinaryGrid(BaseGrid):

    def __init__(self, rows, cols):
        BaseGrid.__init__(self, rows, cols, False)

    def on(self, x, y):
        self.lights[self._index(x, y)] = True

    def off(self, x, y):
        self.lights[self._index(x, y)] = False

    def toggle(self, x, y):
        index = self._index(x, y)
        self.lights[index] = not self.lights[index]

    def is_on(self, value):
        return value == True

class BrightnessGrid(BaseGrid):

    def __init__(self, rows, cols):
        BaseGrid.__init__(self, rows, cols, 0)

    def on(self, x, y):
        self.lights[self._index(x, y)] += 1

    def off(self, x, y):
        index = self._index(x, y)
        value = self.lights[index]

        self.lights[index] = max(0, value - 1)

    def toggle(self, x, y):
        self.lights[self._index(x, y)] += 2

    def is_on(self, value):
        return value > 0



def unfold_range(start, end):
    x1, y1 = start
    x2, y2 = end

    for x in range(x1, x2 + 1):
        for y in range(y1, y2 + 1):
            yield (x, y)

def parse_instruction(raw):
    type = "toggle"
    if "turn on" in raw:
        type = "on"
    elif "turn off" in raw:
        type = "off"

    ranges = list(map(int, re.findall("\d+", raw)))

    start = ranges[0], ranges[1]
    end = ranges[2], ranges[3]

    return type, start, end


if __name__ == '__main__':
    import sys

    if sys.argv[1] == "binary":
        grid = BinaryGrid(1000, 1000)
    else:
        grid = BrightnessGrid(1000, 1000)


    instructions = sys.stdin.readlines()

    for type, start, end in map(parse_instruction, instructions):
        op = getattr(grid, type)
        for x, y in unfold_range(start, end):
            op(x, y)

    print("{} lights are lit".format(grid.count_on()))
