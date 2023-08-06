from ._martini import Martini
from ._datacube import DataCube
from ._demo import demo
from ._version import __version__

__doc__ = """
Mock APERTIF-like Radio Telescope Interferometry of the Neutral ISM
MARTINI is a modular package for the creation of synthetic resolved HI line
observations (data cubes) of smoothed-particle hydrodynamics simulations of
galaxies. The various aspects of the mock-observing process are divided
logically into sub-modules handling the data cube, source, beam, noise,
spectral model and SPH kernel. MARTINI is object-oriented: each sub-module
provides a class (or classes) which can be configured as desired. For most
sub-modules, base classes are provided to allow for straightforward
customization. Instances of each sub-module class are then given as parameters
to the Martini class. A mock observation is then constructed by calling a
handful of functions to execute the desired steps in the mock-observing
process.
The package is functional and (an old version) has been used in:
Oman, K. A., Marasco, A., Navarro, J. F., Frenk, C. S., Schaye, J., Benitez-
Llambay, A. 2019, MNRAS, 482, 821.
Stable releases are available via PyPI (`pip install astromartini`) and the
numbered branches on github. The github master branch is under active
development: things will change, bugs will happen. Any feedback is greatly
appreciated.
Martini does not support use with python2.
See the help for martini.Martini for an example script to configure MARTINI
and create a datacube. This example can be run by doing:
from martini import demo
demo()
Martini has (so far) been successfully run on the output of these simulations:
 - EAGLE
 - APOSTLE
 - C-EAGLE/Hydrangea
 - Illustris
 - IllustrisTNG
 - Augiga
 - MaGICC (and therefore in principle NIHAO)
 - Magneticum
I attempt to support publicly available simulations with a customized source
module. If your simulation is public and not supported, please contact me at
the address below. Currently custom source modules exist for:
 - EAGLE (martini.sources.EAGLESource)
 - IllustrisTNG (martini.sources.TNGSource; also works with Illustris)
If your use of MARTINI leads to a publication, please acknowledge this and link
to the github page, ideally specifying the version used (git commit ID or
version number).
Suport available via kyle.a.oman@durham.ac.uk.
Installation Notes available on https://github.com/kyleaoman/martini, or
https://kyleaoman.github.io/martini/build/html/index.html
"""
