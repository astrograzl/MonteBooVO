#!python
# coding: utf-8
"""MonteBoo Virtual Observatory & Munipack Artificial Sky"""


import subprocess as sub
from flask import render_template


def about():
    """About page with version information"""
    subs = {"shell": True, "stdout": sub.PIPE, "universal_newlines": True}
    muni = sub.run("munipack --version", **subs)
    fits = sub.run("fitspng --version", **subs)
    data = {"muni": muni.stdout, "fits": fits.stdout}
    return render_template("about.html", content=data)


# -------------------------------------------------------------------------- #
# "THE BEER-WARE LICENSE" (Revision 42):                                     #
# <janak@physics.muni.cz> wrote this file. As long as you retain this notice #
# you can do whatever you want with this stuff. If we meet some day, and you #
# think this stuff is worth it, you can buy me a beer in return Zdeněk Janák #
# -------------------------------------------------------------------------- #
