from setuptools import setup
from setuptools import find_packages

version_py = "FullMatrix/_version.py"
exec(open(version_py).read())

setup(
    name="FullMatrix", # Replace with your own username
    version=__version__,
    author="Benxia Hu",
    author_email="hubenxia@gmail.com",
    description="full matrix coordinates",
    long_description="make a full matrix for each chromsome",
    url="https://pypi.org/project/FullMatrix/",
    entry_points = {
        "console_scripts": ['FullMatrix = FullMatrix.FullMatrix:main']
        },
    python_requires = '>=3.6',
    packages = ['FullMatrix'],
    install_requires = [
        'numpy',
        'pandas',
        'argparse',
    ],
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
    zip_safe = False,
  )