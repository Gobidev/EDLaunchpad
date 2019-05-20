import sys

try:
    import launchpad_py as launchpad
except ImportError:
    try:
        import launchpad
    except ImportError:
        sys.exit("error loading launchpad.py")


lp = launchpad.LaunchpadMk2()

lp.Open()
lp.ButtonFlush()
lp.LedAllOn(0)


def rgb(r, g, b):
    r = int(round(r / 255 * 63, 0))
    g = int(round(g / 255 * 63, 0))
    b = int(round(b / 255 * 63, 0))
    return r, g, b


def colorgradient(col1, col2, state):
    r1, g1, b1 = col1
    r2, g2, b2 = col2

    step = round((g2 - g1) / 8)

    rnew = 102
    gnew = round(g1 + state * step)
    bnew = 0

    return rnew, gnew, bnew


def display(amount):
    for y in range(8):
        r, g, b = colorgradient(rgb(102, 0, 0), rgb(102, 102, 0), y + 1)
        r = int(r)
        g = int(g)
        b = int(b)
        for x in range(8):
            if 8 * y + x < amount:
                lp.LedCtrlXY(x, y + 1, r, g, b)
