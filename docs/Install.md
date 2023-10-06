# Installation

Follow the steps below to install `PyStoAnalyzer` locally.

## Create a virtual environment

Create and activate a virtual environment

```bash
python -m venv tester_env

. env/bin/activate
```

## Install dependencies

`PyStoAnalyzer` uses modern `Python` packaging and can be installed using `pip` -

```
python -m pip install PyStoAnalyzer
```
### Setting-up Project 
To use the software properly setup these *API keys* to completely use the features of the 
project:

1. `Newsapi` access from [this](https://newsapi.org/).
2. `Polygon.io` API access from [this](https://polygon.io/).

#### Setup API Globally
```
#Polyon API KEY
export api_key="YOUR-API-KEY"

#NewsApi KEY
export news_api="YOUR-API-KEY"

```
## Build PyStoAnalyzer from source

If you want to develop `PyStoAnalyzer`, or use its latest commit (!can be unstable!),
you might want to install it from the source -

- Clone this repository

```bash
git clone https://github.com/Akhil-Sharma30/PyStoAnalyzer
```

- Change directory

```bash
cd PyStoAnalyzer
```

- Install the package in editable mode with the "dev" dependencies

```bash
python -m pip install -e ".[dev]"
```

Feel free to read our
[Contributing Guide](https://github.com/Akhil-Sharma30/PyStoAnalyzer/blob/main/CONTRIBUTING.md)
for more information on developing `PyStoAnalyzer`.