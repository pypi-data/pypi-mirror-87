# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['fcmeans']

package_data = \
{'': ['*']}

install_requires = \
['jax>=0.2.6,<0.3.0', 'jaxlib>=0.1.57,<0.2.0']

setup_kwargs = {
    'name': 'fuzzy-c-means',
    'version': '1.2.1',
    'description': '',
    'long_description': '# fuzzy-c-means\n\n![GitHub](https://img.shields.io/github/license/omadson/fuzzy-c-means.svg)\n[![PyPI](https://img.shields.io/pypi/v/fuzzy-c-means.svg)](http://pypi.org/project/fuzzy-c-means/)\n[![GitHub commit activity](https://img.shields.io/github/commit-activity/w/omadson/fuzzy-c-means.svg)](https://github.com/omadson/fuzzy-c-means/pulse)\n[![GitHub last commit](https://img.shields.io/github/last-commit/omadson/fuzzy-c-means.svg)](https://github.com/omadson/fuzzy-c-means/commit/master)\n[![Downloads](https://pepy.tech/badge/fuzzy-c-means)](https://pepy.tech/project/fuzzy-c-means)\n[![DOI](https://zenodo.org/badge/186457481.svg)](https://zenodo.org/badge/latestdoi/186457481)\n\n\n`fuzzy-c-means` is a Python module implementing the [Fuzzy C-means][1] clustering algorithm.\n\n## instalation\nthe `fuzzy-c-means` package is available in [PyPI](https://pypi.org/project/fuzzy-c-means/). to install, simply type the following command:\n```\npip install fuzzy-c-means\n```\n\n## basic usage\nsimple example of use the `fuzzy-c-means` to cluster a dataset in tree groups:\n```Python\n%matplotlib inline\n\nfrom fcmeans import FCM\nfrom sklearn.datasets import make_blobs\nfrom matplotlib import pyplot as plt\n\n\n# create artifitial dataset\nn_samples = 5000\nn_bins = 3  # use 3 bins for calibration_curve as we have 3 clusters here\ncenters = [(-5, -5), (0, 0), (5, 5)]\n\nX,_ = make_blobs(n_samples=n_samples, n_features=2, cluster_std=1.5,\n                  centers=centers, shuffle=False, random_state=42)\n\n# fit the fuzzy-c-means\nfcm = FCM(n_clusters=3)\nfcm.fit(X)\n\n# outputs\nfcm_centers = fcm.centers\nfcm_labels  = fcm.u.argmax(axis=1)\n\n\n# plot result\nf, axes = plt.subplots(1, 2, figsize=(11,5))\naxes[0].scatter(X[:,0], X[:,1], alpha=.1)\naxes[1].scatter(X[:,0], X[:,1], c=fcm_labels, alpha=.1)\naxes[1].scatter(fcm_centers[:,0], fcm_centers[:,1], marker="s", s=100, c=\'white\')\nplt.show()\n```\n\n## how to cite fuzzy-c-means package\nif you use `fuzzy-c-means` package in your paper, please cite it in your publication.\n```\n@software{dias2019fuzzy,\n  author       = {Madson Luiz Dantas Dias},\n  title        = {fuzzy-c-means: An implementation of Fuzzy $C$-means clustering algorithm.},\n  month        = may,\n  year         = 2019,\n  publisher    = {Zenodo},\n  doi          = {10.5281/zenodo.3066222},\n  url          = {https://git.io/fuzzy-c-means}\n}\n```\n\n### citations\n - [Gene-Based Clustering Algorithms: Comparison Between Denclue, Fuzzy-C, and BIRCH](https://doi.org/10.1177/1177932220909851)\n\n\n## contributing\n\nthis project is open for contributions. here are some of the ways for you to contribute:\n - bug reports/fix\n - features requests\n - use-case demonstrations\n\nto make a contribution, just fork this repository, push the changes in your fork, open up an issue, and make a pull request!\n\n## contributors\n - [Madson Dias](https://github.com/omadson)\n - [Dirk Nachbar](https://github.com/dirknbr)\n - [Alberth Florêncio](https://github.com/zealberth)\n\n[1]: https://doi.org/10.1016/0098-3004(84)90020-7\n[2]: http://scikit-learn.org/\n',
    'author': 'Madson Dias',
    'author_email': 'madsonddias@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/omadson/fuzzy-c-means',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
