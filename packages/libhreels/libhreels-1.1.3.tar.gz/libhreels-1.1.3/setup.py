# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['libhreels']

package_data = \
{'': ['*']}

install_requires = \
['PyQt5>=5.13,<6.0',
 'argparse>=1.4.0,<2.0.0',
 'matplotlib>=3.2,<4.0',
 'numpy>=1.18.2,<2.0.0',
 'requests>=2.23.0,<3.0.0',
 'scipy>=1.4,<2.0']

extras_require = \
{':python_version < "3.8"': ['importlib-metadata>=1.0,<2.0']}

entry_points = \
{'console_scripts': ['calchreels = libhreels.calcHREELS:myMain',
                     'dielectrics = libhreels.dielectrics:myMain',
                     'viewhreelstest = libhreels.ViewHREELS:myMain'],
 'gui_scripts': ['viewauger = libhreels.ViewAuger:myMain',
                 'viewhreels = libhreels.ViewHREELS:myMain']}

setup_kwargs = {
    'name': 'libhreels',
    'version': '1.1.3',
    'description': 'Handling, simulating, and plotting HREELS and Auger spectroscopy data',
    'long_description': '# HREELS data handling and simulation\n\nSet of data analysis routines for surface vibrational spectroscopy based on a Delta05 spectrometer. Simple data reading and plotting routines are provided, but also advanced routines for in depth analysis.\n\nA fast data browser as graphical user interface is included as **ViewHREELS.py**. It can also take command line arguments.\n\nAdditional a python interface to a Fortran-based calculation of full HREEL spectra is provided in **class lambin** (in **calcHREELS.py**). Note that this part requires a local compilation (via f2py3) from the Fortran90 files. Only for the Linux-based python version 3.6, there are complied files provided. For details see below.\n\nMost of the routines are within the **class HREELS** (HREELS.py). A simple command line program is "showHREELS.py", which reads one data file and plots the spectrum with a second amplified trace.\n\n    Usage:  >python showHREELS.py filename [factor wavenumber]\n\n        E.g.: python showHREELS.py H9H03 100 53 \n\nMore general usage:\n\nRead dataset by calling the HREELS class:\n    **data1 = HREELS(\'filename\', datapath=\'datapath\')**        # Here you can omit the extension \'.gph\'\n                                                    # The second argument is optional\n                                                    \n    This will assign/calculate the following properties:\n    \n    data1.filename\n    data1.datapath\n    data1.startTime\n    data1.stopTime\n    data1.totalTime\n    data1.timePerChannel\n    data1.numberOfSegments\n    data1.energy    # Electron kinetic energy\n    data1.filament  # Filament current in Ampere\n    data1.segments  # list of segment info\n    data1.data      # [(-100.1021616, 259.5), (-98.5374352, 264.5), ...]\n    data1.xdata\n    data1.ydata\n    data1.maxIntensity  # Count rate of elastic peak\n    data1.resolution    # width of elastic peak\n\nThe following methods are defined within the class:\n\n    info()      :   Print information about the spectrum\n    plot()      :   Draws the spectrum. Optional arguments are:\n                    (xmin=None, xmax=None, factor=1, label=\'x\', normalized=False, color="b-",marker=True)\n\n    plotInfoAmp()   Draws spectrum together with amplified trace.\n    pickPeak()  :   Select peak by mouse cursor. The call of figure() is required before.\n    selectData():   Returns the data between wavenumbers x1 and x2\n    findIndex(lossenergy): Returns the data array index for a given energy loss\n    setMarker(x, y, ymin=0, size=None): Sets vertical marker with text label \n    plotWaterFall(...):\n        \n\n# calcHREELS\n\nThese routines are based on the publication "Computation of the surface electron-energy-loss spectrum in specular geometry for an arbitrary plane-stratified medium" by P. Lambin, J.-P. Vigneron, and A. A. Lucas, in the Journal "Computer Physics Communications 60, 351-64(1990)".\n\n\n\n',
    'author': 'Wolf Widdra',
    'author_email': 'wolf.widdra@physik.uni-halle.de',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://gitlab.informatik.uni-halle.de/e3fm8/libhreels',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
