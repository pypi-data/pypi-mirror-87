#  Copyright (c) 2020 Data Spree GmbH - All Rights Reserved
#  Unauthorized copying of this file, via any medium is strictly prohibited.
#  Proprietary and confidential.

from setuptools import setup

setup(
    name='dlds-client',
    version='1.1.0',
    author="Eric Dörheit",
    author_email="eric.doerheit@data-spree.com",
    description="Python API for Deep Learning DS from Data Spree.",
    packages=[
        'dlds.decoder'
    ],
    py_modules=[
        'dlds.dlds_cli',
        'dlds.dlds_client',
        'dlds.dlds_data_loader',
        'dlds.dlds_model',
        'dlds.dlds_worker',
        'dlds.http_token_authentication'
    ],
    install_requires=[
        'Click',
        'joblib',
        'requests',
        'tqdm',
    ],
    extras_require={
        'kitti': ['Pillow'],
        'worker': ['aiofiles', 'aiohttp', 'aiohttp_cors', 'Pillow']
    },
    entry_points='''
        [console_scripts]
        dlds=dlds.dlds_cli:cli
    ''',
    python_requires='>=3.6'
)
