import sys
from EDSM import refresh

try:
    import launchpad_py as launchpad
except ImportError:
    try:
        import launchpad
    except ImportError:
        sys.exit("error loading launchpad.py")

try:
    lp = launchpad.LaunchpadMk2()
except:
    try:
        lp = launchpad.Launchpad()
    except:
        try:
            lp = launchpad.LaunchpadPro()
        except:
            sys.exit("No valid Launchpad detected")

lp.Open()
lp.ButtonFlush()
lp.LedAllOn(0)


def button_press():
    while 1:
        press = lp.ButtonStateXY()
        if press:
            if press[0] == 0 and press[1] == 0:
                refresh()


def rgb(r, g, b):
    r = int(round(r / 255 * 63, 0))
    g = int(round(g / 255 * 63, 0))
    b = int(round(b / 255 * 63, 0))
    return r, g, b


def color_gradient(col1, col2, state):
    r1, g1, b1 = col1
    r2, g2, b2 = col2

    step = round((g2 - g1) / 8)

    red_new = 102
    green_new = round(g1 + state * step)
    blue_new = 0

    return red_new, green_new, blue_new


def display(amount):
    lp.LedAllOn(0)
    for y in range(8):
        r, g, b = color_gradient(rgb(102, 0, 0), rgb(102, 102, 0), y + 1)
        r = int(r)
        g = int(g)
        b = int(b)
        for x in range(8):
            if 8 * y + x < amount:
                lp.LedCtrlXY(x, y + 1, r, g, b)


# display(2)
