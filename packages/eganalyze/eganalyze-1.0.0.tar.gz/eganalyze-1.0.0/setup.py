from setuptools import setup


setup(
    name='eganalyze',
    version='1.0.0',
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
