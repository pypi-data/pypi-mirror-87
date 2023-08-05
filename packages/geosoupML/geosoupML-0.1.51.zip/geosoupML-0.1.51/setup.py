from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="geosoupML",
    version="0.1.51",
    author="Richard Massey",
    author_email="rm885@nau.edu",
    license='Apache License 2.0',
    description="Machine Learning support for geosoup",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/masseyr/geosoupML",
    packages=find_packages(),
    classifiers=[
        'Topic :: Scientific/Engineering :: GIS',
        'Intended Audience :: Science/Research',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',


    ],
    install_requires=[
        'psutil',
        'h5py',
        'numpy',
        'scikit-learn',
        'scipy',
        'geosoup'
    ],
    keywords='geospatial raster vector global spatial regression hierarchical samples random',
)
