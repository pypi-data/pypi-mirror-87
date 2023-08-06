# JAVEC
Just another virtual environment creator

## Installation

Install with pip

    python3 -m pip install javec


## Usage

### No arguments
If you run main.py with no additional arguments:

    javec

It will create virtual environment in current working directory with the same name as current working directory, but with dot in front (hidden file in Linux). To run the virtual environment run:

    source ./.virenvFolder/bin/activate

### -a
Running main.py with -a argument:

    javec -a

In addition to creation of virtual environment it causes creation of script shell named ".activator.sh". Now activation of virtual environment will require running following code:

    source .activator.sh

### -g, --gitignore
Running main.py with -g argument:

    javec -g

In addition to creation of virtual environment it causes creation of .gitignore file. The .gitignore file is a copy of gitignore_example provided in the repository. It was taken from [this repository](https://github.com/github/gitignore).

### --swap-gitignore \<path\>
It is possible to change the gitignore_example from this repository file with one you commonly use by using --swap-gitignore path:

    javec --swap-gitignore /path/to/your/own/.gitignore

If used with -g argument the first action will be swapping gitignore_example and then creation of .gitignore in the current working directory.

### -i, --install \<packages\>
Install given packages. This argument will simply call the following command:

    /path/to/virtualenvironment/bin/python3 -m pip install <packages>

Moreover packages names will be added to requirements_javec.txt file. There is no need to previously activate the virtual environment but you have to call
it from the parent directory(where JAVEC created the virtual environment)

### -r, -u, --remove, --uninstall \<packages\>
Uninstall given packages. This will simply call the following command:

    /path/to/virtualenvironment/bin/python3 -m pip uninstall -y <packages>

Moreover packages names will be removed from requirements_javec.txt file. There is no need to previously activate the virtual environment but you have to call
it from the parent directory(where JAVEC created the virtual environment)

### --versionRequirements
Create requirements.txt file with package version number. This calls following command:

    /path/to/virtualenvironment/bin/python3 -m pip freeze

The output is then filtered with package names installed with this tool (from requirements_javec.txt). requirements.txt will contain only package names that
you installed using JAVEC.

## Have fun!

[![forthebadge made-with-python](http://ForTheBadge.com/images/badges/made-with-python.svg)](https://www.python.org/)