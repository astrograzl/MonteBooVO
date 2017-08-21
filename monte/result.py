#!python
# coding: utf-8
"""MonteBoo Virtual Observatory & Munipack Artificial Sky."""


import os
from time import time
from flask import session, redirect, render_template


def result():
    """Show Result page with artificial frame."""
    if session.get("reset", False):
        return redirect("/proces", code=307)

    if session.get("proces", False):
        return redirect("proces")

    data = session.get("data", {})
    if data.get("name", False):
        id = session["id"]
        if os.path.exists("static/{}.png".format(id)):
            data["img"] = "/static/{}.png?{}".format(id, int(time()))
        else:
            data["img"] = "/static/images/moffat.png"
        if os.path.exists("static/{}.fits.fz".format(id)):
            data["fit"] = "/static/{}.fits.fz?{}".format(id, int(time()))
        else:
            data["fit"] = "#"
        session["data"] = data
        session.modified = True
        return render_template("result.html", data=data)

    return redirect("/index")


# -------------------------------------------------------------------------- #
# "THE BEER-WARE LICENSE" (Revision 42):                                     #
# <janak@physics.muni.cz> wrote this file. As long as you retain this notice #
# you can do whatever you want with this stuff. If we meet some day, and you #
# think this stuff is worth it, you can buy me a beer in return Zdeněk Janák #
# -------------------------------------------------------------------------- #
