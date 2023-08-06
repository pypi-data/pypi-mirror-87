# Weatherstation API Client
This library provides access to the [Wasserschutzpolizei Zurich](https://data.stadt-zuerich.ch/dataset/sid_wapo_wetterstationen) live (using this [JSON API](https://tecdottir.herokuapp.com/docs/)) and historic (using these [CSV files](https://github.com/jelleschutter/fhnw-ds-weatherstation-client/tree/data/history/)) weather data.

## Install
This package builds on Python 3.
```bash
sudo pip3 install fhnw_ds_weatherstation_client
```

## Download Historic Data
```bash
mkdir data && cd data
wget https://raw.githubusercontent.com/jelleschutter/fhnw-ds-weatherstation-client/data/history/messwerte_mythenquai_2007-2019.csv
wget https://raw.githubusercontent.com/jelleschutter/fhnw-ds-weatherstation-client/data/history/messwerte_mythenquai_2020.csv
wget https://raw.githubusercontent.com/jelleschutter/fhnw-ds-weatherstation-client/data/history/messwerte_tiefenbrunnen_2007-2019.csv
wget https://raw.githubusercontent.com/jelleschutter/fhnw-ds-weatherstation-client/data/history/messwerte_tiefenbrunnen_2020.csv
cd ..
```

## Usage
You need to run this code with Python 3 and make sure you adapt *config.historic_data_folder* based on your environment if necessary (default is ./data).
```python
# import the library
import fhnw_ds_weatherstation_client as weather
# import os

# DB and CSV config
config = weather.Config()
# define CSV path (you need to define this based on your environment)
# config.historic_data_folder='.'+os.sep+'data'
# set batch size for DB inserts (decrease for raspberry pi)
# config.historic_data_chunksize=10000
# define DB host
# config.db_host='localhost'

# connect to DB
weather.connect_db(config)
# clean DB
weather.clean_db(config)
# import historic data
weather.import_historic_data(config)
# import latest data (delta between last data point in DB and current time)
weather.import_latest_data(config)
```

## Credits
- [@markif](https://github.com/markif/) - Initial Development
- [@jelleschutter](https://github.com/jelleschutter/) - Further Development