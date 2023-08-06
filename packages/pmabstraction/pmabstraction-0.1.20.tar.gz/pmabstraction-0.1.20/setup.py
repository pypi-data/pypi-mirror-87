from os.path import dirname, join

from setuptools import setup

import pmabstraction


def read_file(filename):
    with open(join(dirname(__file__), filename)) as f:
        return f.read()


setup(
    name=pmabstraction.__name__,
    version=pmabstraction.__version__,
    description=pmabstraction.__doc__.strip(),
    long_description=read_file('pmabstraction/README.md'),
    long_description_content_type="text/markdown",
    author=pmabstraction.__author__,
    author_email=pmabstraction.__author_email__,
    py_modules=[pmabstraction.__name__],
    include_package_data=True,
    packages=['pmabstraction'],
    url='https://github.com/madhubs08/simplify.git',
    license='GPL 3.0',
    install_requires=[
        'pm4py==1.3.0'
    ],
    project_urls={
        'Source': 'https://github.com/madhubs08/simplify.git'
    }
)
