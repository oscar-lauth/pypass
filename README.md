# PyPass

PyPass is a command line password manager. Your PyPass vault is unlocked with a master password you create when first running the application. Your master password is hashed and salted with SHA-512. Passwords you add to your PyPass vault are stored in an sqlite3 database and each password is encrypted with AES encryption.

## Demo

Demo of PyPass being run

<img src="https://s7.gifyu.com/images/pypass-demo.gif" width="1000" height="519">
<!-- ![pypass-demo.gif](https://s7.gifyu.com/images/pypass-demo.gif) -->

## Prerequisites

Both Python 3 and pip3 are required for PyPass. Instructions for installing [Python 3](https://realpython.com/installing-python/) and [pip3](https://pip.pypa.io/en/stable/installing/) linked.

You can check your version of Python 3 and pip3 in terminal with the following commands
```
$ python3 --version
```
```
$ pip3 --version
```


## Getting Started

In terminal, create and navigate to the directory you wish to install PyPass to
```
$ mkdir pypass
$ cd ~/pypass
```
Install PyPass
```
$ git clone https://github.com/oscar-lauth/pypass.git
```
## Setting up venv

It is recommended to install packages and run Python within a virtual environment.

Create a venv in the pypass/ directory 
```
$ python3 -m venv venv
```
Activate venv
```
$ source venv/bin/activate
```
## Installing packages
PyPass utilizes the pycryptodome package to encrypt stored passwords with AES encryption

Install pycryptodome using pip3 inside venv
```
(venv)$ pip3 install pycryptodome
```
Deactivate venv when finished
```
(venv)$ deactivate
```

## Run PyPass
You are now ready to run PyPass

Open terminal and navigate to pypass directory
```
$ cd ~/pypass
```
Activate venv
```
$ source venv/bin/activate
```
Startup PyPass
```
(venv)$ python3 pypass_main.py
```
If it is your first time running PyPass you will be prompted to create a master password

After validating your master password, the PyPass vault will display menu options and allow you to use PyPass

After quitting PyPass with the **qp** command, be sure to deactivate the venv
```
(venv)$ deactivate
```

## Authors

* **Oscar Lauth** - *All work* - [oscar-lauth](https://github.com/oscar-lauth)

## Liability?

* Any liability statemnt
Maybe regarding security and encryption

