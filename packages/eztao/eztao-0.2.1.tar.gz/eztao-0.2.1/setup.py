# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['eztao', 'eztao.carma', 'eztao.ts', 'eztao.viz']

package_data = \
{'': ['*']}

install_requires = \
['celerite>=0.4.0,<0.5.0',
 'matplotlib>=3.3.1,<4.0.0',
 'numba>=0.51.2,<0.52.0',
 'numpy>=1.19.1,<2.0.0',
 'scipy>=1.5.2,<2.0.0']

setup_kwargs = {
    'name': 'eztao',
    'version': '0.2.1',
    'description': 'A toolkit for Active Galactic Nuclei (AGN) time-series analysis.',
    'long_description': '![tests](https://github.com/ywx649999311/EzTao/workflows/tests/badge.svg)\n# EzTao (易道)\n**EzTao** is a toolkit for conducting AGN time-series/variability analysis, mainly utilizing the continuous-time auto-regressive moving average model (CARMA)\n\n## Installation\n```\npip install eztao\n```\n### Dependencies\n>```\n>python = "^3.7"\n>numpy = "^1.19.1"\n>celerite = "^0.4.0"\n>matplotlib = "^3.3.1"\n>scipy = "^1.5.2"\n>numba = "^0.51.2"\n>```\n\n### Quick Examples\nLet\'s first simulate a DRW/CARMA(1,0) process with a variance of 0.3^2 and a relaxation timescale of 100 days. This time series will have a total of 200 data points and span 10 years.\n```python\nimport numpy as np\nimport matplotlib.pyplot as plt\nfrom eztao.carma import DRW_term\nfrom eztao.ts import gpSimRand\n\n# define kernel\namp = 0.3\ntau = 100\nDRW_kernel = DRW_term(np.log(amp), np.log(tau))\nt, y, yerr = gpSimRand(DRW_kernel, 10, 365*10, 200)\n\n# now, plot it\nfig, ax = plt.subplots(1,1, dpi=150, figsize=(8,3))\nax.errorbar(t, y, yerr, fmt=\'.\')\n...\n```\n![drw_sim](include/DRW_sim.jpg)\n\nWe can fit the simulated time series to the DRW model and see how well we can recover the input parameters.\n```python\nfrom eztao.ts import drw_fit\n\nbest_fit = drw_fit(t, y, yerr)\nprint(f\'Best-fit DRW parameters: {best_fit}\')\n```\n```shell\nBest-fit DRW parameters: [0.32236277 106.37368799]\n```\n\nHow does the power spectrum density (PSD) compare?\n```python\nfrom eztao.carma import gp_psd\n\n# get psd functions\ntrue_psd = gp_psd(DRW_kernel)\nbest_psd = gp_psd(DRW_term(*np.log(best_fit)))\n\n# plot\nfig, ax = plt.subplots(1,1, dpi=150, figsize=(6,3))\nfreq = np.logspace(-5, 2)\nax.plot(freq, true_psd(freq), label=\'Input PSD\')\nax.plot(freq, best_psd(freq), label=\'Best-fit PSD\')\n...\n```\n![drw_psd](include/drw_psd.jpg)\n\n__Note:__ How well the input and best-fit PSD match is up to how good the best-fit parameters are, which is highly influenced by the quality of the input time series. \n\nFor more examples, please check out the tutorial folder. \n\n### Development\n`poetry` is used to solve dependencies and to build/publish this package. Below shows how setup the environment for development (assuming you already have `poetry` installed on your machine). \n\n1. Clone this repository, and enter the repository folder.\n2. Create a python virtual environment and activate it. \n    ```\n    python -m venv env\n    source env/bin/activate\n    ```\n3. Install dependencies and **EzTao** in editable mode.\n   ```\n   poetry install\n   ```\n\nNow you should be ready to start adding new features. Be sure to checkout the normal practice regarding how to use `poetry` on its website. When you are ready to push, also make sure the poetry.lock file is checked-in if any dependency has changed. \n',
    'author': 'Weixiang Yu',
    'author_email': 'wy73@drexel.edu',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/ywx649999311/EzTao',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
