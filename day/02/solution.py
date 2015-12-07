def parse_dimensions(present):
    present = present.strip()

    l, w, h = map(int, present.split('x'))

    return l, w, h

def calculate_sides(l, w, h):
    return (
        l * w,
        w * h,
        h * l
    )

def calculate_wrapping(l, w, h):
    sides = calculate_sides(l, w, h)
    slack = min(sides)

    return sum(map(lambda x: 2 * x, sides)) + slack

def calculate_total_wrapping(presents):
    dimensions = map(parse_dimensions, presents)
    return sum(map(lambda d: calculate_wrapping(*d), dimensions))

def calculate_ribbon(l, w, h):
    min_sides = sorted([l, w, h])[:2]

    return sum(map(lambda x: 2 * x, min_sides)) + l * w * h

def calculate_total_ribbon(presents):
    dimensions = map(parse_dimensions, presents)
    return sum(map(lambda d: calculate_ribbon(*d), dimensions))


if __name__ == '__main__':
    import sys

    presents = sys.stdin.readlines()

    print("The Presents need {} square feet of wrapping".format(
            calculate_total_wrapping(presents)))
    print("The presents need {} feet of ribbon".format(
            calculate_total_ribbon(presents)))

