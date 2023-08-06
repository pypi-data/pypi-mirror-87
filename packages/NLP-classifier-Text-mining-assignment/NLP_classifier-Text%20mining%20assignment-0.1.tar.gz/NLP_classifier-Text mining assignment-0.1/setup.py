import setuptools
from setuptools import setup, find_packages

setup(
    name='NLP_classifier-Text mining assignment',
    version='0.1',
    url='https://github.com/Taiinguyenn139/NLPTextClassifier',
    author='Duy Khang and Thanh Tai',
    author_email='taiinguyenn139@gmail.com',
    description="Vietnamese Newspapaper classifier",
    long_description="Vietnamese Newspapaper classifier with 10 topics",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6'
)


