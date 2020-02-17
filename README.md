# COP3502:Moss

This is a simple extract, organize, and submit script to make use of [Stanford Moss](https://theory.stanford.edu/~aiken/moss/) to catch potential plagrisim through [moss.py](https://github.com/soachishti/moss.py). This was originally written for COP3502 at the University of Florida, but can be expanded upon and altered for different use cases.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites
Developed with [Python](https://www.python.org/downloads/) 3.6.9

Packages:  
- [moss.py](https://github.com/soachishti/moss.py): Used to interface with the Moss system.
- [mossum](https://github.com/hjalti/mossum): Optional: Used to generate graphics represent Moss matches.

In order to use the Moss system, you will need a user id. Instructions for that can be found on main page for [Moss](https://theory.stanford.edu/~aiken/moss/).

Additionally, this project uses [pipenv](https://github.com/pypa/pipenv) to install the above packages and to load .env for the Moss user id.

### Installing

Quick and simple with pipenv

```
pipenv install
```

Otherwise

``` bash
pip3 install moss.py
pip3 install git+https://github.com/hjalti/mossum@master
```

#### Additional for mossum
To render graphics, mossum uses dot via graphiz. This needs to be installed in order to use mossum.

Ubuntu
```
sudo apt-get install graphviz
```

## Running

### Python
1. organize_submissions.py handles extracting the zip file of the students' submissions into individual folders index by said student's name.
```
python3 organize_submissions.py
```
2. moss.py handles uploading students' submission into Moss, dowloading the report, and generating the mossum graphic.
```
python3 moss.py
```

### Downloading students' submissions from Zybooks
The "Download submissions" button can be found under "Lab statistics and submissions" in each assignment.  
The line
``` python
config['submissions_archive'] =  "resources/archive2.zip"
```
needs to be updated to the point to this downloaded file. 

## Acknowledgments

* [JKomskis](https://github.com/JKomskis)
* [rhoroff](https://github.com/rhoroff)

Built off of their work.

## Errors:
- No such file or directory: 'out/mossum/report-1.png'
    - The directories leading to the file need to be created beforehand. In this case out/mossum directory needs to exist before mossum can generate the report-1.png file