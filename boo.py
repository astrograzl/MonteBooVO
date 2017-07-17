#!python
# coding: utf-8
# @uthor: janak
"""MonteBoo Virtual Observatory & Munipack Artificial Sky"""

import os
import subprocess as sub
from string import capwords
from astropy import units as u
from flask import Flask, flash, session, request, redirect, render_template
from monte import coordination, catalogue, artificial, fitspng


app = Flask(__name__)
app.secret_key = os.urandom(24)


@app.route("/")
@app.route("/index")
def index():
    """Index page with search input"""
    return render_template("index.html")


@app.route("/about")
def about():
    """About page with version information"""
    subs = {"shell": True, "stdout": sub.PIPE, "universal_newlines": True}
    muni = sub.run("munipack --version", **subs)
    fits = sub.run("fitspng --version", **subs)
    data = {"muni": muni.stdout, "fits": fits.stdout}
    return render_template("about.html", content=data)


@app.route("/result", methods=["GET", "POST"])
def result():
    """Result page with artificial frame and debug listing"""
    if request.method == "GET":
        if not session.get("reset", False):
            if session.get("data", False):
                return render_template("result.html", data=session["data"])
            flash("There is none artificial frame right now.")
            return redirect("/index")
        else:
            name = session.get("data")["obj"]
            session["reset"] = False
            session.modified = True
            flash("The frame was updated based on the new settings.")
    elif request.method == "POST":
        name = request.form["object"]
    coor = coordination(name)
    if coor is None:
        flash("Can't find required object. Please try another one.")
        return render_template("index.html")
    status = catalogue(coor)
    if status:
        flash("This is really bad. Looks like zombies shutdown the server.")
        return redirect("/index")
    output = artificial(coor, session.get("setup", {}))
    imname, finame = fitspng()
    data = {"obj": capwords(name),
            "ra": coor.ra.to_string(unit=u.hourangle, sep=":"),
            "dec": coor.dec.to_string(unit=u.degree, sep=":", alwayssign=True),
            "out": output,
            "img": imname,
            "fit": finame}
    session["data"] = data
    session["reset"] = False
    session.modifies = True
    return render_template("result.html", data=data)


@app.route("/setup", methods=["GET", "POST"])
def setup():
    """Setup page with options configuration"""
    if request.method == "POST":
        session["setup"] = request.form
        session["setin"] = 0
        for k in request.form.keys():
            if request.form[k]:
                session["setin"] += 1
        if request.form["psf"] == "SEEING":
            session["setin"] -= 1
        if request.form["spread"] == "FFT":
            session["setin"] -= 1
        session["reset"] = True
        session.modified = True
        flash("Saved the settings. Now go and check the new image.")
    form = session.get("setup", {})
    return render_template("setup.html", form=form)


@app.route("/setup/reset")
def reset():
    """Setup page after reseting settings"""
    session["setin"] = 0
    session["setup"] = {}
    session["reset"] = True
    session.modified = True
    flash("Reset settings to their default values.")
    return redirect("/setup")


@app.errorhandler(404)
def error(err):
    """Page Not Found"""
    flash(err)
    return render_template("error.html"), 404


if __name__ == "__main__":
    app.run(debug=True)


# -------------------------------------------------------------------------- #
# "THE BEER-WARE LICENSE" (Revision 42):                                     #
# <janak@physics.muni.cz> wrote this file. As long as you retain this notice #
# you can do whatever you want with this stuff. If we meet some day, and you #
# think this stuff is worth it, you can buy me a beer in return Zdeněk Janák #
# -------------------------------------------------------------------------- #
