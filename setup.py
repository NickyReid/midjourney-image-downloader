import os
from setuptools import setup

requirements = ["requests"]

if not os.path.isdir("jobs"):
    os.makedirs("jobs")

setup(
    name='midjourney-image-downloader',
    version='0.0.1',
    packages=[''],
    url='',
    license='MIT',
    author='nicky',
    author_email='nicky.reid92@gmail.com',
    description='Download images from your Midjourney gallery',
    install_requires=requirements
)
