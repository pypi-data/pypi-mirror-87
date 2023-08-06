from setuptools import setup,find_packages

with open("README.md",'r') as fh:
    long_description=fh.read()

setup(
    name="kanoapi",
    version="0.13.0",
    author="DTMKEN",
    author_email="jlijian83@gmail.com",
    description="1.Change Packages name(kanoapi) bilibili:单推manKen,PyPi:DTMKEN",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ken-kano/",
    install_requires=[
        "pygame","easygui","requests","you-get",
    ],
    packages=find_packages(),
   classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
