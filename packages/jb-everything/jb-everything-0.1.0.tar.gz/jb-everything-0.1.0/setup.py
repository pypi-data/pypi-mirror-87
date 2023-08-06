from setuptools import setup

setup(
    name='jb-everything',
    version='0.1.0',
    packages=['jb_everything'],
    url='https://pypi.org/project/jb-everything/',
    license='MIT',
    author='jeromebaum',
    author_email='jerome@jeromebaum.com',
    description='Large list of imports for machine learning.',
    install_requires=[
        'numpy~=1.19.4',
        'scipy~=1.5.3',
        'scikit-learn~=0.23.2',
        'pandas~=1.1.4',
        'lightgbm~=3.1.0',
        'matplotlib~=3.3.3',
        'seaborn~=0.11.0',
        'xarray~=0.16.2',
        'missingno~=0.4.2',
        'dabl~=0.1.9',
        'eli5~=0.10.1',
        'dask~=2.30.0',
        'jax~=0.2.7',
        'requests~=2.25.0',
    ],
)
