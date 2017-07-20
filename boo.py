#!python
# coding: utf-8
"""MonteBoo Virtual Observatory & Munipack Artificial Sky"""


import subprocess as sub
from string import capwords
from secrets import token_urlsafe
from astropy import units as u
from astropy.coordinates import SkyCoord
from flask import Flask, flash, session, request, redirect, render_template
from monte import coordination, catalogue, artificial, fitspng, default


app = Flask(__name__)
app.secret_key = token_urlsafe(24)
app.jinja_env.trim_blocks = True
app.jinja_env.lstrip_blocks = True


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
    """Result page with artificial frame"""
    if request.method == "POST":
        if request.form["type"] == "search":  # search widget
            search = True
            click = False
            name = request.form["name"]

            coor = coordination(name)
            if coor is None:
                flash("Can't find required object. Please try another one.")
                return redirect("/index")

            session["cat"] = catalogue(coor)
            session.modified = True
            if session["cat"]["retcode"] != 0:
                flash("This is really bad :-( " +
                      "Looks like zombies shutdown the server.")
                return redirect("/index")

        elif request.form["type"] == "button":  # click on button
            click = True
            search = False
            ra = session["data"]["ra"]["deg"]
            dec = session["data"]["dec"]["deg"]
            name = session["data"]["name"]
            coor = SkyCoord(ra=ra, dec=dec, unit=u.degree)

        if search or (click and session.get("reset", False)):
            session["art"] = artificial(coor, session.get("config", {}))
            session["reset"] = False
            session.modified = True

        imname, finame = fitspng()  # always reload saved image

        # update stored data in session
        data = {"name": capwords(name),
                "ra": {"deg": coor.ra.deg,
                       "str": coor.ra.to_string(unit=u.hourangle, sep=":")},
                "dec": {"deg": coor.dec.deg,
                        "str": coor.dec.to_string(unit=u.degree, sep=":")},
                "img": imname,
                "fit": finame}
        session["data"] = data
        session.modified = True

        return render_template("result.html", data=data)

    if request.method == "GET":
        data = session.get("data", {})
        if data.get("name", False):
            return render_template("result.html", data=data)
        return redirect("/index")


@app.route("/config", methods=["GET", "POST"])
def config():
    """Setup parameters with options configuration"""
    if not session.get("config", False):
        session["config"] = {}
    if request.method == "POST":
        setin = 0
        setup = request.form.to_dict()
        del setup["token"]
        for field in setup:
            if setup[field]:
                setin += 1
        if "psf" in setup and setup["psf"] == "SEEING":
            setin -= 1
        if "spread" in setup and setup["spread"] == "FFT":
            setin -= 1
        session["setin"] = setin
        session["config"] = setup
        session["reset"] = True
        session.modified = True
    form = session.get("config", {})
    return render_template("config.html", form=form, default=default,
                           token=token_urlsafe(32))


@app.route("/config/reset")
def reset():
    """Setup page after reseting settings"""
    session["setin"] = 0
    session["config"] = {}
    session["reset"] = True
    session.modified = True
    return redirect("/config")


@app.errorhandler(Exception)
def error(err):
    """Do not panic"""
    flash(err)
    return render_template("error.html")


@app.errorhandler(404)
def notfound(err):
    """Page Not Found"""
    flash(err)
    return render_template("notfound.html"), 404


@app.route("/debug")
def debug():
    """Show verbose debug output"""
    data = session.get("data", {})
    if data.get("name", False):
        return render_template("debug.html", session=session)
    return redirect("/index")


if __name__ == "__main__":
    app.run(debug=True)


# -------------------------------------------------------------------------- #
# "THE BEER-WARE LICENSE" (Revision 42):                                     #
# <janak@physics.muni.cz> wrote this file. As long as you retain this notice #
# you can do whatever you want with this stuff. If we meet some day, and you #
# think this stuff is worth it, you can buy me a beer in return Zdeněk Janák #
# -------------------------------------------------------------------------- #
