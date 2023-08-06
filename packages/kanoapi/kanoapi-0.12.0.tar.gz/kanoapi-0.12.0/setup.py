from setuptools import setup,find_packages

with open("README.md",'r') as fh:
    long_description=fh.read()

setup(
    name="kanoapi",
    version="0.12.0",
    author="DTMKEN",
    author_email="jlijian83@gmail.com",
    description="1.Fixed some kano-official.amebaownd.com No Viewer and return empty.(WARNING:The only can requests NEWS&Information pages,if you do not like this packages Please Back to version 0.1.150)   b站:单推manKen,PyPi:DTMKEN",
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