# Modula modbus connection server
This repository contains a server that permits the control
of an Odoo instance that is linked to a Modula Slim machine
within Smart Factory. 

## Dependencies
The project only requires an installation of Python 3.10, as 
well as Pipenv to manage package dependencies. If not already installed,
Pipenv can be installed through the following command:

```bash
pip install pipenv
```

## Installation
The following command will install the locked Pipenv dependencies from the
Pipfile.lock file:
```bash
pipenv install
```

TODO: running instructions

## Configuration
When the server is first run, a config.toml file will be created at the root of the
repository. This file contains the required parameters for the server to run. Of 
particular importance are the following:
- hostname
- port
- odoo user
- odoo password