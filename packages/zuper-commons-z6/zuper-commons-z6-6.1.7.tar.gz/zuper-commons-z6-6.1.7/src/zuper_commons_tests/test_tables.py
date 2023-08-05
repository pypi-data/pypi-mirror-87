import math
import random

from nose.tools import assert_raises

from zuper_commons.text.table import format_table, wrap_lines
from zuper_commons.text.text_sidebyside import pad
from zuper_commons.ui import color_ops


def test_table1():
    cells = {}

    r = lambda T: random.randint(0, T)
    for _ in range(20):
        i = r(5)
        j = r(5)

        cells[(i, j)] = ("blah" * r(3) + "\n") * r(3)

    T = {}
    styles = ["pipes", "heavy", "light", "circo"]
    for i, style in enumerate(styles):
        for j, light_inside in enumerate((True, False)):
            T[(i, j)] = format_table(cells, style=style, color="red", light_inside=light_inside)

    s = format_table(T, style="light", color="yellow", light_inside=False)
    print(s)


def test_wrap_lines():
    wrap_lines("adepoak opdk apokde opak dpokeapo k", 10)


def test_pad():
    text = """

deioj iojea iojae 
doew
odewp okwedpo kpwe 
    
    """
    identity = lambda _: _
    style_funs = [identity, color_ops]
    for style_fun in style_funs:
        for halign in ["left", "center", "right"]:
            for valign in ["top", "bottom", "middle"]:
                for linelength in [10, 80]:
                    nlines = 10

                    pad(text, nlines, linelength, halign, valign, style_fun)


def test_pad1():
    text = """

deioj iojea iojae 
doew
odewp okwedpo kpwe 

    """
    identity = lambda _: _
    pad(text, 3, 20, "left", "top", identity)

    assert_raises(ValueError, pad, text, 20, 20, "XXX", "top", identity)
    assert_raises(ValueError, pad, text, 20, 20, "left", "XXX", identity)
