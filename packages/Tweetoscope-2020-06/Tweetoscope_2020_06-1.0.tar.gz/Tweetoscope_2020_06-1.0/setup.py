from setuptools import setup, find_packages
import sys, os

version = '1.0'
requirements = """kafka-python
termcolor
twine
""".split('\n')

setup(
    name='Tweetoscope_2020_06',
    version=version,
    description='Tweetoscope',
    author='Anass Elidrissi',
    author_email='anasselidrissi97@gmail.com',
    url=
    'https://gitlab-student.centralesupelec.fr/tweetoscope-mullticolore/tweetou',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    entry_points={
        'console_scripts': [
            'learner = ml.learner:main',
            'hawkes = ml.hawkes:main',
        ],
    },
    install_requires=requirements,
)
