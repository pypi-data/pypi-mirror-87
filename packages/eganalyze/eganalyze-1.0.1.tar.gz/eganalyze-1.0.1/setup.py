from setuptools import setup
from eganalyze import __version__


setup(
    name='eganalyze',
    version=__version__,
    packages = ['eganalyze'],
    author='Kevin Kennell',
    author_email='kevin@kennell.de',
    license='MIT',
    url='https://github.com/kennell/eganalyze',
    install_requires=[
            'click',
            'pandas'
    ],
    entry_points={
        'console_scripts': [
            'eganalyze = eganalyze.cli:main'
        ]
    }
)
