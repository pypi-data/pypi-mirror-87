import pathlib
from setuptools import setup, find_packages

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name='naviml',
    version='0.0.6',
    description="Navi the Navigator",
    long_description=README,
    long_description_content_type="text/markdown",
    url = "https://github.com/claudiolau/naviml",
    license="MIT",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'Click','Pandas'
    ],
    entry_points='''
        [console_scripts]
        naviml = navi:cli
    ''',
    
    python_requires='>=3.6',    
)