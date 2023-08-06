from setuptools import setup, find_packages

with open('README.md') as readme_file:
    README = readme_file.read()

with open('HISTORY.md') as history_file:
    HISTORY = history_file.read()

setup(
    name='flights_time_series_dataset',
    version='1.0.1',
    description='Flights time series dataset for time-series-predictor.',
    long_description_content_type="text/markdown",
    long_description=README + '\n\n' + HISTORY,
    license='The Unlicense',
    packages=find_packages(exclude=("tests",)),
    author='Daniel Kaminski de Souza',
    author_email='daniel@kryptonunite.com',
    keywords=['Time series dataset'],
    url='https://github.com/krypton-unite/flights_time_series_dataset.git',
    download_url='https://pypi.org/project/flights-time-series-dataset/',
    install_requires = [
        'time-series-dataset',
        'pandas',
        'seaborn'
    ],
    extras_require={
        'test': [
            'pytest',
            'pytest-cov'
        ],
        'dev': [
            'bumpversion',
            'twine',
            'wheel',
            'pylint',
            'autopep8'
        ]
    }
)