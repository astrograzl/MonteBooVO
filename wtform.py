#!python
# coding: utf-8
# @uthor: janak
"""MonteBoo Virtual Observatory & Munipack Artificial Sky"""


from flask_wtf import FlaskForm
from wtforms import DecimalField, IntegerField, StringField,\
                    DateField, RadioField, BooleanField

# https://stackoverflow.com/questions/1305532/convert-python-dict-to-object
class Struct:
    """Convert python dict to object"""
    def __init__(self, **entries):
        self.__dict__.update(entries)


class MyForm(FlaskForm):
    """Setup form"""
    psf = RadioField("Point spreed function",
                     choices=[("SEEING", "seeing"),
                              ("MOFFAT", "moffat"),
                              ("GAUSS", "gauss")])
    spread = RadioField("Seeing spread method",
                        choices=[("FFT", "fft"),
                                 ("RANDOM", "random"),
                                 ("AUTO", "auto")])
    hwhm = DecimalField("Half width at half of maximum",
                        render_kw={"placeholder": "1"})
    airy = DecimalField("Radius of Airy spot",
                        render_kw={"placeholder": "0.1"})
    beta = DecimalField("Moffat exponent",
                        render_kw={"placeholder": "2"})
    maglim = DecimalField("Magnitude limit",
                          render_kw={"placeholder": "13"})
    back_level = DecimalField("Backgound level",
                              render_kw={"placeholder": "1000"})
    back_noise = DecimalField("Background noise",
                              render_kw={"placeholder": "31.6"})
    back_grad_x = DecimalField("Background gradient in x",
                               render_kw={"placeholder": "0"})
    back_grad_y = DecimalField("Background gradient in y",
                               render_kw={"placeholder": "0"})
    area = DecimalField("Area of input aperture",
                        render_kw={"placeholder": "1"})
    diameter = DecimalField("Diameter of input aperture",
                            render_kw={"placeholder": "1.1"})
    exptime = DecimalField("Exposure time",
                           render_kw={"placeholder": "1"})
    qeff = DecimalField("Quantum efficiency",
                        render_kw={"placeholder": "1"})
    atmosphere = BooleanField("Apply atmosphere modelling")
    extk = DecimalField("Extinction coefficient",
                        render_kw={"placeholder": "0"})
    long = DecimalField("Geographic longitude of station (-east)",
                        render_kw={"placeholder": "0"})
    lat = DecimalField("geographic latitude of station (+north)",
                       render_kw={"placeholder": "0"})
    date = DateField("Initial date",
                     render_kw={"placeholder": "2000-01-01"})
    time = StringField("Initial time",
                       render_kw={"placeholder": "00:00:00.000"})
    fov = DecimalField("Field of view",
                       render_kw={"placeholder": "0.2"})
    scale = DecimalField("Scale", render_kw={"placeholder": "1/3600"})
    angle = DecimalField("Angle", render_kw={"placeholder": "0"})
    width = IntegerField("Width of output", render_kw={"placeholder": "666"})
    height = IntegerField("Height of Output", render_kw={"placeholder": "666"})


text = {"psf": "seeing", "spread": "fft", "hwhm": "pix", "airy": "pix", "beta": "",
        "maglim": "", "back_level": "cts", "back_noise": "cts",
        "back_grad_x": "cts/pix", "back_grad_y": "cts/pix",
        "area": "m2", "diameter": "m", "exptime": "s", "qeff": "",
        "atmosphere": "extinction, seeing", "extk": "",
        "long": "deg", "lat": "deg", "date": "YYYY-MM-DD", "time": "HH:MM:SS",
        "fov": "deg", "scale": "deg/pix", "angle": "deg",
        "width": "pix", "height": "pix"}


class Struct:
    def __init__(self, **entries):
        self.__dict__.update(entries)
