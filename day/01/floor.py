def calculate_floor(instructions):
    floor = 0
    first_basement_entry = 0

    for pos, instruction in enumerate(instructions):
        if instruction == '(':
            floor += 1
        elif instruction == ')':
            floor -= 1
        else:
            raise ValueError("Did not expect instruction " + instruction)

        if floor == -1 and first_basement_entry == 0:
            first_basement_entry = pos + 1

    return floor, first_basement_entry

if __name__ == '__main__':
    import sys

    instructions = sys.stdin.read().strip()
    floor, first_basement_entry = calculate_floor(instructions)

    print(instructions)
    print("Results in floor {}".format(floor))
    print("Basement entry at {}".format(first_basement_entry))

