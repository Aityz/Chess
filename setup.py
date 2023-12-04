from setuptools import setup, find_packages

setup(
    name='aityz_chess',
    version='1.1.3',
    packages=find_packages(include=['aityz_chess', 'aityz_chess.*']),
    install_requires=[
        'chess',
        'matplotlib',
        'requests',
        'stockfish',
        'pillow'
    ],
    python_requires='>=3.6',
    url='https://github.com/Aityz/Chess',
    license='MIT',
    description='A Python package for analysing chess.com games.',
    long_description=open('README.md').read(),)
