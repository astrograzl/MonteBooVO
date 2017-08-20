#!python
# coding: utf-8
"""MonteBoo Virtual Observatory & Munipack Artificial Sky."""


from secrets import token_urlsafe
from flask import Flask, flash, session, redirect, render_template
import monte

app = Flask(__name__)
app.secret_key = token_urlsafe(24)
app.jinja_env.trim_blocks = True
app.jinja_env.lstrip_blocks = True


@app.route("/")
@app.route("/index")
def index():
    """Show Index page with search input."""
    return render_template("index.html")


@app.route("/about")
def about():
    """Show About page with version information."""
    return monte.about()

@app.route("/coord", methods=["GET", "POST"])
def coord():
    """Process coordination question and catalogue download"""
    return monte.coord()


@app.route("/proces", methods=["GET", "POST"])
def proces():
    """Process request about artificial frame"""
    return monte.proces()


@app.route("/result")
def result():
    """Show Result page with artificial frame."""
    return monte.result()


@app.route("/config", methods=["GET", "POST"])
def config():
    """Show Setup parameters with options configuration."""
    return monte.config()


@app.route("/config/reset")
def reset():
    """Show Setup page after reseting settings."""
    return monte.reset()


@app.route("/config/export")
def export():
    """Export configuration to file"""
    if session.get("config", False):
        return monte.export()
    return redirect("/config")


@app.route("/debug")
def debug():
    """Show verbose debug output."""
    data = session.get("data", {})
    if data.get("name", False):
        return render_template("debug.html")
    return redirect("/index")


@app.errorhandler(404)
def notfound(err):
    """Show Page Not Found."""
    flash(err)
    return render_template("notfound.html"), 404


@app.errorhandler(Exception)
def error(err):
    """Do not panic."""
    flash(err)
    return render_template("error.html"), 666


if __name__ == "__main__":
    app.run(debug=True)


# -------------------------------------------------------------------------- #
# "THE BEER-WARE LICENSE" (Revision 42):                                     #
# <janak@physics.muni.cz> wrote this file. As long as you retain this notice #
# you can do whatever you want with this stuff. If we meet some day, and you #
# think this stuff is worth it, you can buy me a beer in return Zdeněk Janák #
# -------------------------------------------------------------------------- #
