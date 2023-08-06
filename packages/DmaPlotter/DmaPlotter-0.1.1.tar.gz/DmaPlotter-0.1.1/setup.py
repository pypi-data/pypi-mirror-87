from setuptools import setup, find_packages
import pathlib

here = pathlib.Path(__file__).parent.resolve()

setup(
    name='DmaPlotter',

    version='0.1.1',

    description='A one-function tool for visualizing metrics by DMA on a US map',

    author='Bart Massi', 

    classifiers=[  
        'Development Status :: 3 - Alpha',

        'Intended Audience :: Developers',

        # Pick your license as you wish
        'License :: OSI Approved :: MIT License',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate you support Python 3. These classifiers are *not*
        # checked by 'pip install'. See instead 'python_requires' below.
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3 :: Only',
    ],

    install_requires=['numpy', 
    'requests',
    'matplotlib',
    'shapely',
    'plotly'],

)