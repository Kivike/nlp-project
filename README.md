# Natural Language Processing - Crime prediction using hotel customer reviews

## Requirements

* [Python 3][python-site]
* [pip][pip-site]
* [virtualenv][virtualenv-install-site] (optional)
* [Docker][docker-site] (optional)

## Getting started

Please note that virtual environment is not mandatory; you can install project dependencies globally on your machine in case you find it suitable for you (see step 5).

1. Clone the repo by issuing `git clone https://....`
2. `cd` into the repository root
3. Create a virtual environment into the project root: `python3 -m venv env` 
   * It will create a directory called `env` which will be used to store dependencies
   * In case you want to explicitly select Python version see [this][venv-help-1] and [this][venv-help-2]
   * Please note that it **will not** install a new version of Python; you can merely select which installation from your machine you want to use in this virtual environment
4. Activate the created environment by running `source env/bin/activate` on Unix or `.\env\Scripts\activate` on Windows
5. Install dependencies from [requirements.txt](requirements.txt) by issuing `pip install -r requirements.txt`
   * In case you want to install other dependencies later on, you can just install them by issuing `pip install ...` and then update the requirements file by issuing `pip freeze > requirements.txt`
6. Now you should have proper Python environment activated and project dependencies installed
7. Leave the virtual environment by issuing `deactivate`

The `env` directory is not supposed to be version controlled. Dependencies are managed through `requirements.txt` file, and it's completely possible to opt out of virtual environment and just install dependencies globally. Please refer to the official [virtualenv documentation][virtualenv-install-site] for more information on how to use it.

## Sourcing GeoJSON data

As the task in the project is to investigate criminal activity and hotel reviews in London metropolitan area, we focus in London. Spatial clustering is part of the project, and requires dividing geographical areas in some manner for graphical representation of data on a map. We logically chose the post codes for that purpose; each post code district (or sector) is one area on the map. For that purpose, we need some GeoJSON files describing those areas. The following steps describes how this can be done.

1. The data can be found from [Edinburgh Data Share][geojson-data]
   * It is initally in shapefiles, and contains all post code areas, districts and sectors for whole UK
2. Convert the `.shp` files into `GeoJSON` by using the [ogr2ogr.sh](./geoutils/ogr2ogr.sh) script
   * Please note that this requires Docker installed; in case you don't have it, you can try to install the [gdal][gdal-site] tool on your machine and follow the instructions on the script
   * The data is initially divided into three levels: areas, districts and sectors. You can convert any one of them; see the [examples](./geoutils/examples/README.md) for more details about the levels.
3. Now you have some GeoJSON files containing the whole UK area. Use the [london_codes.py](./geoutils/london_codes.py) script to generate the final GeoJSON for London area.
   * The script will filter out post code areas outside of london and save the result in a new file
    ```bash
    python ../../geoutils/london_codes.py --in PostalArea.geojson --out ../geojson/london/PostalArea.geojson
    ```



[python-site]:https://www.python.org/
[pip-site]:https://pypi.org/project/pip/
[virtualenv-install-site]:https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/
[venv-help-1]:https://stackoverflow.com/questions/1534210/use-different-python-version-with-virtualenv
[venv-help-2]:https://stackoverflow.com/questions/1534210/use-different-python-version-with-virtualenv/39713544#39713544
[docker-site]:https://www.docker.com/
[geojson-data]:https://datashare.is.ed.ac.uk/handle/10283/2597
[gdal-site]:https://gdal.org/
