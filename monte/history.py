#!python
# coding: utf-8
"""MonteBoo Virtual Observatory & Munipack Artificial Sky."""

import os
from glob import glob
from random import choice
from flask import redirect, render_template


def history():
    """Display overwiev of history to be forgotten."""
    hist = glob("static/*.fits.gz")
    assert len(hist) > 0, "You can make choice, only when you have any ;-)"
    while True:
        fits = choice(hist)
        sid = fits.rstrip(".fits.gz")
        if os.path.exists(sid+".png") and\
           os.path.exists(sid+".svg") and\
           os.path.exists(sid+".fits.fz"):
            return render_template("history.html", sid=sid)
    return redirect("/history")


# -------------------------------------------------------------------------- #
# "THE BEER-WARE LICENSE" (Revision 42):                                     #
# <janak@physics.muni.cz> wrote this file. As long as you retain this notice #
# you can do whatever you want with this stuff. If we meet some day, and you #
# think this stuff is worth it, you can buy me a beer in return Zdeněk Janák #
# -------------------------------------------------------------------------- #
