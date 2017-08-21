#!python
# coding: utf-8
"""MonteBoo Virtual Observatory & Munipack Artificial Sky."""


import os
from time import time
from flask import session, redirect, render_template
from matplotlib import pyplot as plt
from astropy.io import fits


def stars():
    """Plot star chart from catalogue data"""
    id = session.get("id", "")
    sess = session.get("data", {})
    if sess.get("name", "Random") != "Random" and len(id) > 0:
        co = "static/{}.fits.gz".format(id)
        if os.path.exists(co):
            data = fits.getdata(co)
            plt.figure(figsize=(8, 8))
            plt.xlabel("$\\alpha$")
            plt.ylabel("$\\delta$")
            plt.grid(True)
            plt.gca().invert_xaxis()
            plt.scatter(data["RAJ2000"], data["DEJ2000"],
                        s=2**data["Vmag"]/1024, c=data["Jmag"]-data["Vmag"])
            plt.savefig("static/{}.svg".format(id), bbox_inches="tight")
            session["data"]["svg"] = "static/{}.svg?{}".format(id, int(time()))
            session.modified = True
            return render_template("stars.html", data=session.get("data", {}))
        return redirect("/debug")
    return redirect("/index")


# -------------------------------------------------------------------------- #
# "THE BEER-WARE LICENSE" (Revision 42):                                     #
# <janak@physics.muni.cz> wrote this file. As long as you retain this notice #
# you can do whatever you want with this stuff. If we meet some day, and you #
# think this stuff is worth it, you can buy me a beer in return Zdeněk Janák #
# -------------------------------------------------------------------------- #
