# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['tess_sip']

package_data = \
{'': ['*']}

install_requires = \
['astropy>3.2.3',
 'lightkurve>=2.0b3',
 'numpy>1.18.2',
 'scipy>1.5.3',
 'tqdm>4.41.1']

setup_kwargs = {
    'name': 'tess-sip',
    'version': '1.0.2',
    'description': "Demo tool for creating a Systematics-insensitive Periodogram (SIP) to detect long period rotation in NASA's TESS mission data.",
    'long_description': '# TESS SIP \n<a href="https://doi.org/10.5281/zenodo.4291096"><img src="https://zenodo.org/badge/DOI/10.5281/zenodo.4291096.svg" alt="DOI"></a>\n\nDemo tool for creating a Systematics-insensitive Periodogram (SIP) to detect long period rotation in NASA\'s TESS mission data. \n\n## What is SIP\n\nSIP is a method of detrending telescope systematics simultaneously with calculating a Lomb-Scargle periodogram. You can read a more in-depth work of how SIP is used in NASA\'s Kepler/K2 data [here](https://ui.adsabs.harvard.edu/abs/2016ApJ...818..109A/abstract). \n\n\n## Usage\n\nThis repository contains a demo notebook for how to calculate a SIP for NASA CVZ targets. To use this demo, you can either download and run the notebook, or re-write/copy the scripts in the notebook in your own tools. \n\n![Example SIP output](https://github.com/christinahedges/TESS-SIP/blob/master/demo.png?raw=true)\n\n\n## Requirements\n\nTo run this demo you will need to have [lightkurve](https://github.com/keplerGO/lightkurve) installed, with a minimum version number of v2.0.\n\n## Acknowledgements\n\nThis tool uses the [lightkurve](https://github.com/keplerGO/lightkurve) tool to build a SIP, and relies on the `RegressionCorrector` and `SparseDesignMatrix` lightkurve tools. The SIP project was developed in part at the `online.tess.science` meeting, which took place globally in 2020 September. This research made use of [Astropy](http://www.astropy.org.) a community-developed core Python package for Astronomy.',
    'author': 'Christina Hedges',
    'author_email': 'christina.l.hedges@nasa.gov',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
