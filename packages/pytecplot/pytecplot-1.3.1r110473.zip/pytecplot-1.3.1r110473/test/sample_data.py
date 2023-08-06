import base64
import os
import zlib

from contextlib import contextmanager
from tempfile import NamedTemporaryFile

import numpy as np

from numpy import random as rand

import tecplot as tp
from tecplot.exception import *
from tecplot.constant import *


data = {
    # Rectangular Dataset 10x10x10
    # tecplot plt format (2016), gzip'd and base64 encoded
    '10x10x10' : r'''\
H4sICBHvNFcAA3JlY3QxMHgxMHgxMC5wbHQA7ZexSsRAEIYjdhY+gYViZ3dWXmFSnCC2IqJ2IRds
ROE8C63uCa7zJXKdr6QP4BvoDJmDIAh/49h8Ax+b3f2zO7t/SDb7excnl6PR4UbRx5lxb8yN1phF
vTbugmdj12iiv43+9T3T6J8O2utoewzNPObbNK7i+jrKmyiLxevkPPTNYBzP59Z4inzqyMPHfzEe
QtPGMF8RxaBe/IitAf3cbxOf3/dlze/3f1ZKfbx8Px4vm3LVdaVdlx9H29WqO6hmO6eVtZtmgQ4d
OnTo0KFDhw4dOnTo0KH7Y50S/VgKTangOSl43gq+NgVfv4LvkYLvo0K/1wr4gR/4gR/4gR/4gR/4
gR/4gR/4gR/Ef4f+3EMO2vsFclDf45CD+r2EHNRzCeSgnv8gB/WcDTmo/zOQg/7fCBl8AwxKGY9I
MAAA''',

    # Two Rectuangular Datasets 2x2x3
    # "Rectangular zone 1"
    #       range(x,y,z) := [0,1], [0,1], [0,2]
    #       P := X + Y**2 - 0.1 * Z**2
    # "Rectangular zone 2"
    #       range(x,y,z) := [0,1], [0,1], [1,3]
    #       P := X - Y**2 + 0.1 * Z**2
    '2x2x3_overlap' : r'''\
H4sICLy5hlcAA3JlY3QyeDJ4M19vdmVybGFwLnBsdABTVgxxCTM0NGJkgABPIM4D4hIgTgXiIig/
EYhzoLgSiBWAOBkqnwqVh+lJgcqnIIknQsWKoWpKoPaxAHEElB0JpaOgdACUZmiY6hwE1ZeMZB7I
XelAXAp1VyLUPSB7qoA4H6omFSpmCDXuPxQwIPEZ0AATFDNT2Q1GFLlhkzPIHaC4Qsa4zfhgj5/P
4ADEC2bOvLkfiQ+yyJ40GsYmhY8uDpd3QMPIeh3OnjmzNy0tzR6EjY0/2wP5+2bNlLQHYSDbnjrh
A6M5QPYfOHPmDSh8EtLS/pEYLuSED6HwcEDBQD/bnj3TAwqP/RD2GTtj482g8ADx7ZDCCRxuAN+4
w4vwAwAA''',

    # Rectangular Dataset 3x3 with Z=X+Y, and 2x2 with Z=0
    # tecplot plt format (2016), gzip'd and base64 encoded
    '3x3_2x2' : r'''\
H4sIAPXtOVcAA1NWDHEJMzQ0YmSAAE8gzgPiEiBOBeIiKD8RiHOguBKIFYA4GSqfCpWH6UmByqcg
iSdCxYqhakqg9jEDcQSUHQmlo6A0Q8NU5yCo+mQkc0DuSQfiUqh7EqHuAJlfBcT5UDWpULF8qFpk
P4HAfyhgQOIzoAFmKIaFD7XclAnlw8RIcRMTFCPctMkZ5C5GqBgTklpM/R/s8fMZHKA0ULzBngCb
ASEGww1IGBk8sEe1D53/Awcf6B6CfrsAVfvCHjsfGTTYAY20R6VhbAcs6lEBAOeZjTAwAwAA''',


    # Rectangular Dataset 10x10x10 with text-box and circle annotations
    # tecplot plt format (2016), gzip'd and base64 encoded
    '10x10x10_anno' : r'''\
H4sICNfIC1cCA3JlY3QxMHgxMHgxMF90ZXh0X2dlb20ucGx0AO2XQSgEURjHZ60iB6Wc5LDIRVrW
iYN5amRJSpJwW2PaiyhWsZvs1cGeUFyd7JYDzhzFYQ/KxU2kJEVOSq33dr7dXqQ+B8/l/9Vv5833
/rPv+95/m51paRrvn4hEugKWH0OSeUlC4kkW6TwmmSNWJSGJS/MezZeumaX5WS0fo9wSaRK0XlAy
SeMpOk7T0Uq/O6ouRXVws84r7IiBtfj+6fGzsLSoKI/a+9Tn3q6KC/Fx8Ho1MjNa1FZZX+OlmC/I
0LNjVJ+r1a36j0uWqf8Y9a36iUg6JSs/jP0+zh2L+iiukd8IhyofzpqHwye76zflXkq1NJA2SPlU
/WH0NrlV7mdQq9fv9UBcP6XeHvOXQl+no7XKttLbzm97SkoWSONptel79XXfVNRo+H0fOWr9kocB
Tfv9+hfBOe/J3PX2ZFw7l83acmzfd9eKXLZNLDZGhcxLTRo66KCDDjrooIMOOuiggw466KD7Yx0n
/O/i4NocVE0cVN0cVG8cVP8c1B5xUPvIwd9rDvADfsAP+AE/4Af8gB/wA37AD/gBP+AH4r+D/7sH
ZuDdX4AZuPdxYAbu/yUwA/e5BJiB+/wHzMB9zgZm4L7PADPw3xuBCT4Byshp0owxAAA=''',

    # Zones: Rectangular3D, Rectangular2D, Line, Cylinder
    # tecplot plt format (2016), gzip'd and base64 encoded
    '4zones' : r'''\
H4sICL91O1cAA3JlY3QxLTNEX2N5bDNELnBsdABTVgxxCTM0NGJkgABPIM4D4hIgTgXiIig/EYhz
oLgSiBWAOBkqnwqVh+lJgcqnIIknQsWKoWpKoPYxA3EElB0JpaOgNEPDVOcgqPpkJHNA7kkH4lKo
exKh7jAGYheo1v9QwIDEZ0ADzEiYHPuMyLQPFtYg+3yAVCbUjlQSzWJEM8uZARI3OUhmpjAg4pEU
szlQwmWTM8h8mH2MSGox9X+wJ5IPpBvoxWZAiMFwAxKmiRpcwJ4wbiCMqRYfyO6iajhiB2S7GyfA
bzd++xbsufJmP7J9c4ze74fSUDM/oMgj28c+d74d+1x5MLv9zuO97XeS94HYT5c+2/d0adp+dDay
GmS9DDjCe4iaDwcyaifsZNQ8wOIPpvy0ezClEsxmUouzY1K7Zwdl7wOy90HV7AOq2Q/Vuw+odz+6
mUPb/Ib9tMW0BkSUSxRgAAOUr5CMCAAA''',

        '3x3x3_text' : r'''\
TITLE     = "Internally created data set"
VARIABLES = "X"
"Y"
"Z"
ZONE T="Rectangular zone"
 STRANDID=0, SOLUTIONTIME=0
 I=3, J=3, K=3, ZONETYPE=Ordered
 DATAPACKING=BLOCK
 DT=(SINGLE SINGLE SINGLE )
 0.E+00 5.E-01 1.E+00 0.E+00 5.E-01
 1.E+00 0.E+00 5.E-01 1.E+00 0.E+00
 5.E-01 1.E+00 0.E+00 5.E-01 1.E+00
 0.E+00 5.E-01 1.E+00 0.E+00 5.E-01
 1.E+00 0.E+00 5.E-01 1.E+00 0.E+00
 5.E-01 1.E+00
 0.E+00 0.E+00 0.E+00 5.E-01 5.E-01
 5.E-01 1.E+00 1.E+00 1.E+00 0.E+00
 0.E+00 0.E+00 5.E-01 5.E-01 5.E-01
 1.E+00 1.E+00 1.E+00 0.E+00 0.E+00
 0.E+00 5.E-01 5.E-01 5.E-01 1.E+00
 1.E+00 1.E+00
 0.E+00 0.E+00 0.E+00 0.E+00 0.E+00
 0.E+00 0.E+00 0.E+00 0.E+00 5.E-01
 5.E-01 5.E-01 5.E-01 5.E-01 5.E-01
 5.E-01 5.E-01 5.E-01 1.E+00 1.E+00
 1.E+00 1.E+00 1.E+00 1.E+00 1.E+00
 1.E+00 1.E+00
''',

    # Rectangular Dataset 3x3x3 with P=X+Y**2-Z**3
    # tecplot plt format (2016), gzip'd and base64 encoded
    '3x3x3_p' : r'''\
H4sICLLcg1cAA3JlY3QzeDN4M19wLnBsdABTVgxxCTM0NGJkgABPIM4D4hIgTgXiIig/EYhzoLgS
iBWAOBkqnwqVh+lJgcqnIIknQsWKoWpKoPaxAHEElB0JpaOgdACUZmiY6hwE1ZeMZB7IXelAXAp1
VyLUPSB7qoA4H6omFWrMfyhgQOIzoAFmJAyxe5MzyH5Q+CBj3GZ8sCeO/2E/VMABSgPFG+zpxGZA
iMFwAxKmiRpcwJ4wbiACI/uxwQ4YrEB6AZR/ACTvAMT7gGygXAKID6QVgPQEewh/gz0kbhpA8QKN
Gwcg3bAPYh4iDAElY/Z8NAMAAA==''',

    # Rectangular Dataset 3x3x1 with P=X+Y**2
    # tecplot plt format (2016), gzip'd and base64 encoded
    '3x3x1_p' : r'''\
H4sICAplhlcAA3JlY3QzeDN4MV9wLnBsdABTVgxxCTM0NGJkgABPIM4D4hIgTgXiIig/EYhzoLgS
iBWAOBkqnwqVh+lJgcqnIIknQsWKoWpKoPYxA3EElB0JpQOgNEPDVOcgqPpkJHNA7kkH4lKoexKh
7gCZXwXE+VA1qVBj/kMBAxKfAQ0wQzEsHBgaNjmD7GeEijEiqcXU/8EeP5/BAUoDxRvsCbAZEGIw
3ICEkdU32AGNBtILoPwDIHkHAE/k1SjUAQAA''',

    # Rectangular Dataset 3x1x3 with P=X+Z**2
    # tecplot plt format (2016), gzip'd and base64 encoded
    '3x1x3_p' : r'''\
H4sICDNlhlcAA3JlY3QzeDF4M19wLnBsdABTVgxxCTM0NGJkgABPIM4D4hIgTgXiIig/EYhzoLgS
iBWAOBkqnwqVh+lJgcqnIIknQsWKoWpKoPaxAHEElB0JpaOgdACUZmiY6hwE1ZeMZB7IXelAXAp1
VyLUPSB7qoA4H6omFWrMfyhgQOIzoAFmIGaE0hC7NzmD7GeEisMwbjM+2KObSUDeAUoDxRvsCbBJ
AfYI3ICEkc1ssANaD6QXQPkHQPIOACmtvNEUAgAA''',

    # Rectangular Dataset 1x3x3 with P=Y+Z**2
    # tecplot plt format (2016), gzip'd and base64 encoded
    '1x3x3_p' : r'''\
H4sICNVkhlcAA3JlY3QxeDN4M19wLnBsdABTVgxxCTM0NGJkgABPIM4D4hIgTgXiIig/EYhzoLgS
iBWAOBkqnwqVh+lJgcqnIIknQsWKoWpKoPaxAHEElB0JpaOgdACUZmiY6hwE1ZeMZB7IXelAXAp1
VyLUPSB7qoA4H6omFWrMfyhgQOIzoAFQODBDMcTuTc4g+xmhcjCMzwxU8MEeP5/BAb9+FADU22BP
gI2kFoYbkDCy+gY7oPVAegGUfwAk7wAAk14VZxQCAAA=''',

    # 1D Zone with shape (10,1,1) and X in [-10,10]
    # dependent variables: Y=0, P=X, Q=X**2, R=X**3
    'xylines_poly' : r'''\
H4sIANeuyVcAA1NWDHEJMzQ0YmSAAE8gzgPiEiBOBeIiKD8RiHOguBKIFYA4GSqfCpWH6UmByqcg
iSdCxYqhakqg9rECcQSUHQmlA6B0IJQOgtIMDVOdDYGULhC7QM2LAuJ8qBtTocr+QwEDEp8BDXAB
MSMUQ8ze5AwynxFJHEUexRyVA1DaAd1cLPIJpw58tof6EKLeof8AlAbyFQ72Pf5xQOb4xgOhoaEH
nlj07QdieyDbASjmAJQDqXHEbg82QKx5J5zW/ix0uv/ym6PMcUPHYLZ59iAMYoPEQHIgNQwMVUe+
O7w+vK9c+/AbVZFDjlPX7wdieyDbCSjmDJRzBqpxAQCzoG5bSAIAAA==''',

    # 3D Zones with solution times: [0, 1, 2]
    '3x3x3_3zones_time' : r'''\
H4sICHydElwAAzN4M3gzXzN6b25lc190aW1lLnBsdABTVgxxCTM0NGJkgABPIM4D4hIgTgXiIig/
EYhzoLgSiBWAOBkqnwqVh+lJgcqnIIknQsWKoWpKoPYxA3EElB0JpaOgNEPDVOcgqPpkJHNA7kkH
4lKoexKh7gCZXwXE+VA1qVBj/gMBAxJA58PcAcO0s/uD/cDZzeBAnN2bnEH2g9IDDMMApv4P9kTy
gXQDvdgMCDEYbkDCNFGDC9gTxg2E8Wh8kKoGFxiND6xhMbTjAwB6eFPpxAYAAA==''',
}

layouts = {
    '3pt_xyline_text' : r'''#!MC 1410
$!CREATERECTANGULARZONE
  IMAX = 3 JMAX = 1 KMAX = 1
  X1 = 0 Y1 = 0 Z1 = 0
  X2 = 3 Y2 = 1 Z2 = 1
  XVAR = 1 YVAR = 2
$!ALTERDATA
  EQUATION = '{Y} = {X}**2'
$!PLOTTYPE  = XYLINE
$!FRAMENAME  = 'Frame 001'
$!DELETELINEMAPS
$!ACTIVELINEMAPS  =  [1]
$!LINEMAP  [1]
  NAME = '&ZN&'
  ASSIGN { ZONE = 1 XAXISVAR = 1 YAXISVAR = 2 }
  LINES { COLOR = RED }
$!XYLINEAXIS
  DEPXTOYRATIO = 1
$!XYLINEAXIS
  XDETAIL 1 { RANGEMIN = 0 RANGEMAX = 3 GRSPACING = 0.5 }
$!XYLINEAXIS
  YDETAIL 1 { RANGEMIN = 0 RANGEMAX = 9 GRSPACING = 2 }''',
}

images = {
    'swoosh_png': r'''\
iVBORw0KGgoAAAANSUhEUgAAAAoAAAAKCAIAAAACUFjqAAAB73pUWHRSYXcgcHJvZmlsZSB0eXBl
IGV4aWYAAHjanVRbrtwgDP1nFV0CfmBgOUwAqTvo8ntMyO1MNHd0VVsExxgfv5Iw/vye4ZeTZQ2a
crFqFkFatXKDUOJJLj+wGKufqmLxIop1PReFZXyqXw4uPfFNv3dqN0e60enxenDpudwc8bmJA0Am
3Y7qFkigfoNsteSo/97bBpg7RctJreQUrBtzFOEhhsUnmkQhqdLE5QYZB3hGyLyfDrqcQcheox3R
usKCSlXyg0u/EpBdtCe9nI5XsdxXuKcS+Ty4Fx1hvNfHq2u23NNCvYzsfWc+NSZ86sxK66nQqlvi
V33KkcJzeHP2MudYFtrUMKC2J+xKnrYdxlQ9h4RM1DlASKeI3dlQ0gOznTdPzPYD8R5EcRKDfXcS
MjooY1dqgdJSFpwXatTBc7FQZmZlpsGKCwO68RULbdi8gEcsAdgDRgpnSuP/OfzUcM7DS0Trg25r
IS72tniyKLb4BjN0gfKeNYrfk3fSYtk3Jp1dhKO0rsk3V2TNcvLKAhjFSheofnVzD+RbuoyJPkZ3
DU1zR8dOxTP1NKNM/MW0Vjrm0XOqvWKQi5WWJXezUWbW0WNFgI0S7udj1hHGkWsfPXHpo9h8wArh
J31QAvGR8RuVlqfVVmQC3T/Qv+JhKmtcwMjNAAAAA3NCSVQICAjb4U/gAAAAoklEQVQYlX2QMQqD
QBBFx1ktbBa21VY8hdew8YZexFa0tLC3cUVYC5n5pEhIYsC87vOax48A0D38s0XEe3+r53nu+/44
josGAOA8z2VZkiSZpklEPpqZmXldV1U1xoQQQghEFBPRvu9d1+V5vm2biGRZ5pyz1r60tXYYhrZt
i6Ko67osy3dKTESqqqpVVTVNk6bpJRWA934cx2edquKL6P8tDzRbZ6/XavV9AAAAAElFTkSuQmCC''',
}

def sample_data_file(data_id):
    fout = NamedTemporaryFile(suffix='.plt', delete=False)
    if 'text' in data_id:
        fout.write(data[data_id].encode())
    else:
        fout.write(zlib.decompress(base64.b64decode(data[data_id]), 15+32))
    os.fsync(fout)
    fout.close()
    return fout.name
def sample_data(data_id):
    fname = sample_data_file(data_id)
    return fname, tp.data.load_tecplot(fname, read_data_option=ReadDataOption.ReplaceInActiveFrame)
@contextmanager
def saved_sample_data_file(data_id):
    try:
        fname = sample_data_file(data_id)
        yield fname
    finally:
        tp.new_layout()
        try:
            os.remove(fname)
        except Exception as e:
            print(e)
@contextmanager
def loaded_sample_data(data_id):
    with saved_sample_data_file(data_id) as fname:
        yield tp.data.load_tecplot(fname, read_data_option=ReadDataOption.ReplaceInActiveFrame)


def sample_layout_file(data_id):
    fout = NamedTemporaryFile(suffix='.plt', delete=False)
    if 'text' in data_id:
        fout.write(layouts[data_id].encode('utf-8'))
    else:
        fout.write(zlib.decompress(base64.b64decode(data[data_id]), 15+32))
    os.fsync(fout)
    fout.close()
    return fout.name
def sample_layout(data_id):
    fname = sample_layout_file(data_id)
    return fname, tp.load_layout(fname)
@contextmanager
def saved_sample_layout_file(data_id):
    try:
        fname = sample_layout_file(data_id)
        yield fname
    finally:
        tp.new_layout()
        try:
            os.remove(fname)
        except Exception as e:
            print(e)
@contextmanager
def loaded_sample_layout(data_id):
    with saved_sample_layout_file(data_id) as fname:
        yield tp.load_layout(fname)

@contextmanager
def temporary_image_file(image_id, **kw):
    with NamedTemporaryFile(delete=False, **kw) as ftmp:
        try:
            ftmp.write(base64.decode(images[image_id], 15+32))
            ftmp.close()
            yield ftmp.name
        finally:
            os.remove(ftmp.name)


def ensure_dataset(name, variables, frame):
    if frame is None:
        frame = tp.active_page().add_frame()

    if frame.has_dataset:
        dataset = frame.dataset
        vnames = dataset.variable_names
        for v in variables:
            if v not in vnames:
                dataset.add_variable(v)
    else:
        dataset = frame.create_dataset(name, variables)

    return frame, dataset


def create_i_ordered(length=3, frame=None):
    rand.seed(1)
    X = np.linspace(0, 1, length)
    scalar_data = X**2
    scalar_data += rand.normal(0, 0.2, scalar_data.shape)

    with tp.session.suspend():
        fr, ds = ensure_dataset('Data 2D', ['x','s'], frame)
        z = ds.add_ordered_zone(name='I-Ordered Float Nodal {}'.format(length),
                                shape=(length,))
        z.values('x')[:] = X
        z.values('s')[:] = scalar_data
        plot = fr.plot(PlotType.Cartesian2D)
        plot.activate()
        plot.contour(0).variable = ds.variable('s')

    return plot


def create_ordered_2d(shape=(2, 3), frame=None):
    x = np.linspace(0, 1, shape[0])
    y = np.linspace(0, 2, shape[1])
    Y, X = np.meshgrid(y, x, indexing='ij')
    shape = X.shape[::-1]
    rand.seed(1)
    scalar_data = np.sqrt(X**2 + Y**2)
    scalar_data += rand.normal(0, 0.2, scalar_data.shape)

    with tp.session.suspend():
        fr, ds = ensure_dataset('Data 2D', ['x','y','s'], frame)
        z = ds.add_ordered_zone(name='Ordered Float Nodal {}'.format(shape),
                                shape=shape)
        z.values('x')[:] = X
        z.values('y')[:] = Y
        z.values('s')[:] = scalar_data
        plot = fr.plot(PlotType.Cartesian2D)
        plot.activate()
        plot.contour(0).variable = ds.variable('s')

    return plot


def create_ordered_3d(shape=(2, 3, 4), frame=None):
    x = np.linspace(0, 1, shape[0])
    y = np.linspace(0, 2, shape[1])
    z = np.linspace(0, 3, shape[2])
    Z, Y, X = np.meshgrid(z, y, x, indexing='ij')
    shape = Z.shape[::-1]
    X += np.sin(Z)
    rand.seed(1)
    scalar_data = np.sqrt(Y**2 + Z**2)
    scalar_data += rand.normal(0, 0.2, scalar_data.shape)
    u = np.sqrt(Y**2 + Z**2) + rand.normal(0, 0.2, Z.shape)
    v = np.sqrt(X**2 + Z**2) + rand.normal(0, 0.2, Z.shape)
    w = np.sqrt(X**2 + Y**2) + rand.normal(0, 0.2, Z.shape)

    with tp.session.suspend():
        fr, ds = ensure_dataset('Data 3D', ['x','y','z','u','v','w','s'], frame)
        z = ds.add_ordered_zone(name='Ordered Float Nodal {}'.format(shape),
                                shape=shape)
        z.values('x')[:] = X
        z.values('y')[:] = Y
        z.values('z')[:] = Z
        z.values('u')[:] = u
        z.values('v')[:] = v
        z.values('w')[:] = w
        z.values('s')[:] = scalar_data
        plot = fr.plot(PlotType.Cartesian3D)
        plot.activate()
        plot.contour(0).variable = ds.variable('s')

        plot.vector.u_variable = ds.variable('u')
        plot.vector.v_variable = ds.variable('v')
        plot.vector.w_variable = ds.variable('w')

    return plot


def create_polar(frame=None):
    shape = (10,)
    t = np.linspace(0, (180 / np.pi) * 3 * np.pi, 10)
    r = np.linspace(0, 1, 10)

    with tp.session.suspend():
        fr, ds = ensure_dataset('Data Polar', ['t', 'r'], frame)
        z = ds.add_ordered_zone(name='Ordered Float Nodal {}'.format(shape),
                                shape=shape)
        z.values('t')[:] = t
        z.values('r')[:] = r
        plot = fr.plot(PlotType.PolarLine)
        plot.activate()

    return plot


def create_xyline(frame=None):
    shape = (4,)
    x = np.linspace(0, 3, 4)
    y = x**2

    with tp.session.suspend():
        fr, ds = ensure_dataset('Data XY Line', ['x', 'y'], frame)
        z = ds.add_ordered_zone(name='Ordered Float Nodal {}'.format(shape),
                                shape=shape)
        z.values('x')[:] = x
        z.values('y')[:] = y
        plot = fr.plot(PlotType.XYLine)
        plot.activate()

    return plot
