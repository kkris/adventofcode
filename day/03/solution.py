def visit(visited, cell):
    visited.add(cell)

def next(cell, instruction):
    x, y = cell
    if instruction == '^':
        return x, y + 1
    elif instruction == 'v':
        return x, y - 1
    elif instruction == '>':
        return x + 1, y
    elif instruction == '<':
        return x - 1, y
    else:
        raise ValueError("Unexpected instruction {}".format(instruction))

def visit_all(instructions):
    current = (0, 0)
    visited = set([current])

    for instruction in instructions:
        cell = next(current, instruction)
        visit(visited, cell)

        current = cell

    return visited

if __name__ == '__main__':
    import sys

    instructions = sys.stdin.read().strip()

    if sys.argv[1] == 'robot':
        visited = visit_all(instructions[::2])
        visited.update(visit_all(instructions[1::2]))
    else:
        visited = visit_all(instructions)

    print("{} houses were visited".format(len(visited)))
