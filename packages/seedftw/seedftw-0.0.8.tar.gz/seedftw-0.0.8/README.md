# seedftw

This package is meant to give you simple [access to] energy and environment data from the world (in short *seedftw*). This package is meant to be used with Python 3.

## Capabilities

Currently, it contains the following data loading capabilities:
* Energy:
    * Transmission system data from [Denmark](https://www.energidataservice.dk/tso-electricity) under **seedftw.energy.denmark**. This data is provided by the danish transmission system operator Energinet.
* Environment:
    * Simple geographical computations, under **seedftw.environment.geography**
    * Weather observations from [Denmark](https://confluence.govcloud.dk/pages/viewpage.action?pageId=15303111) under **seedftw.environment.denmark**. This data is provided by the Danish Meteorological Institute (DMI). OBS: you need to create an API key on [their portal]((https://confluence.govcloud.dk/display/FDAPI)) to gain access to the data.


## Installation

If you want to get the latest stable version, you can get it via pip, as it is [registered on PyPi](https://pypi.org/project/seedftw/) :
~~~ 
pip install seedftw
~~~

If you want to use the development version, then just keep on using the one in the repository on Gitlab: https://gitlab.com/Pierre_VF/seedftw .


## Examples and documentation

You can find a documentation and code samples in Jupyter notebooks in the *examples* folder.

The installation process for the API keys is provided in these notebooks where relevant.

## Note to users and developers
This repository is currently developed as a hobby project. But if you're interested in contributing, this is very welcome.

At the moment, the documentation is very unevenly advanced, help there is also appreciated.

The style format used for development is [Black](https://pypi.org/project/black/), if you contribute, it would be nice if you remember to apply it to your code before committing.