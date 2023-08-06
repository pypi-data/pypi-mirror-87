# ColabCode

[![license](https://img.shields.io/badge/license-MIT-blue.svg)](/LICENSE)
[![PyPI version](https://badge.fury.io/py/imcode.svg)](https://badge.fury.io/py/imcode)
![python version](https://img.shields.io/badge/python-3.6%2C3.7%2C3.8-blue?logo=python)


## Installation

Installation is easy!

```
$ pip install imcode
```

Run code server on Google Colab or Kaggle Notebooks

## Getting Started


ImCode also has a command-line script. So you can just run `imcode` from command line.

`imcode -h` will give the following:

```
usage: imcode [-h] --port PORT [--password PASSWORD] [--mount_drive]

ImCode: Run VS Code On Colab / Kaggle Notebooks

required arguments:
  --port PORT          the port you want to run code-server on

optional arguments:
  --password PASSWORD  password to protect your code-server from unauthorized access
  --mount_drive        if you use --mount_drive, your google drive will be mounted
```

Else, you can do the following:


```shell
# import imcode
$ from imcode import ImCode

# run imcode with by deafult options.
$ ImCode()

# ImCode has the following arguments:
# - port: the port you want to run code-server on, default 10000
# - password: password to protect your code server from being accessed by someone else. Note that there is no password by default!
# - mount_drive: True or False to mount your Google Drive

$ ImCode(port=10000, password="nitin", mount_drive=True)
```
## How to use it?
Colab starter notebook: [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/imneonizer/imcode/blob/master/colab_starter.ipynb)

`ImCode` comes pre-installed with some VS Code extensions.

## Original project
https://github.com/abhishekkrthakur/colabcode

## License

[MIT](LICENSE)
