
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ppdp_anonops",
    version="0.0.2",
    author="Alexander 'DevSchnitzel' Schnitzler",
    author_email="DevSchnitzel@outlook.com",
    description="A package providing multiple anonymization methods for XES-event logs",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/TheDevSchnitzel/PPDP-AnonOps",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        'kmodes >= 0.10.2',
        'pm4py == 1.2.10',
        'p_privacy_metadata == 0.0.4',
        'matplotlib >= 2.2.2',
        'numpy >= 1.18.1',
        'pycryptodome == 3.9.9',
        'scikit_learn >= 0.23.2'
    ],
    test_suite='nose.collector',
    tests_require=['nose'],
)