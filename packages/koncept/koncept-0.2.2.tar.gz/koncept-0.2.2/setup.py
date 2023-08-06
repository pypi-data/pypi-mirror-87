# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['koncept', 'koncept..ipynb_checkpoints']

package_data = \
{'': ['*']}

install_requires = \
['kuti>=0.9.4,<0.10.0']

setup_kwargs = {
    'name': 'koncept',
    'version': '0.2.2',
    'description': 'Koncept IQA',
    'long_description': '# Koncept Image Quality Assessment Models\n\n```\nfrom kuti import applications as apps\nfrom kuti import generic as gen\nfrom kuti import image_utils as iu\nimport pandas as pd, numpy as np, os, urllib\n\n# download and read the meta-data for the KonIQ-10k IQA database\nkoniq_meta_url = "https://github.com/subpic/koniq/raw/master/metadata/koniq10k_distributions_sets.csv"\nurllib.request.urlretrieve(koniq_meta_url, \'koniq10k_distributions_sets.csv\')\ndf = pd.read_csv(\'koniq10k_distributions_sets.csv\')\n\n# download some images from the test set of the database via direct link\nurl_list = \'http://media.mmsp-kn.de/koniq10k/1024x768/\' + df[df.set==\'test\'].image_name[::50]\ngen.make_dirs(\'tmp/\')\nfor url in url_list:\n    file_name = url.split(\'/\')[-1]\n    urllib.request.urlretrieve(url, \'tmp/\'+file_name)\n\nfrom koncept.models import Koncept512\nk = Koncept512()\n\n# read images and assess their quality\nimages = [iu.read_image(p) for p in \'tmp/\' + df[df.set==\'test\'].image_name[::50]]\nMOS_pred = k.assess(images)\n\n# compare with the ground-truth quality mean opinion scores (MOS)\nMOS_ground = df[df.set==\'test\'].MOS[::50]\napps.rating_metrics(MOS_ground, MOS_pred);\n```',
    'author': 'Vlad Hosu',
    'author_email': 'subpic@gmail.com',
    'maintainer': 'Vlad Hosu',
    'maintainer_email': 'subpic@gmail.com',
    'url': 'https://github.com/subpic/koncept',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6.1,<4.0.0',
}


setup(**setup_kwargs)
