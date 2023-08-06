from setuptools import setup


setup(
    name='dzipf',
    version='0.1',
    author='Damien Irving',
    packages=['dzipf'],
    install_requires=[
        'matplotlib',
        'pandas',
        'scipy',
        'pyyaml',
        'pytest'],
    entry_points={
        'console_scripts': [
            'countwords = dzipf.countwords:main',
            'collate = dzipf.collate:main',
            'plotcounts = dzipf.plotcounts:main']})
