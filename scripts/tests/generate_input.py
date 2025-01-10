import pandas as pd
from pathlib import Path
import requests
import json
from urllib.parse import urlparse
import logging
import re
import os


# set logging config
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s', 
    filename='generate_input.log',
    filemode='w'
)


# function to ensure folder existence
def ensure_folder_exists(folder_path):
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)


# function to flatten nested list
def flatten_and_split(input_list: list) -> list:
    result = []
    for sublist in input_list:
        # Convert the sublist item to string and split by '|'
        result.extend(str(sublist).split('|'))
    # Strip whitespace from each resulting part
    return [item.strip() for item in result if item != 'nan' ]


# function to get marineinfo url in case of dasid
def get_mi_json(wp: str, url: str, output_path: str) -> None:
    """
    1. contructs marineinfo-url based on dasid (which follows 'module=dataset&dasid=' in the url)
    2. retrieves the json record from the marineinfo-url
    3.writes it to a file
    """

    print(url)
    base = urlparse(url).netloc.split('.')[-2]
    dasid = url.split("=")[-1]
    # mi_url = f"http://marineinfo.org/id/dataset/{dasid}.json"

    response = requests.get(f'{url}&show=json')
    if response.status_code == 200:
        try:
            data = response.json()
            file_path = f'{output_path}/{base}_{dasid}.json'
            with open(file_path, 'w') as json_file:
                json.dump(data, json_file, indent=4)
        except json.decoder.JSONDecodeError as e:
            logging.info(f'{wp} - {url} - {e}')

    else:
        print(response.status_code)
        logging.info(f'{wp} - {url} - HTTP Status code:{response.status_code}')


# Analyse datasets
files = list(Path('./input/').glob('MARCO-BOLO_Metadata_Dataset_Record_description_*.csv'))

for wp_file in files:
    wp = wp_file.stem.split('_')[-1]
    print(wp)
    wp_df = pd.read_csv(wp_file)
    wp_urls = flatten_and_split(list(wp_df.DataLandingPageURL))

    for url in wp_urls:
        output_path = f'./input/{wp}_json'
        ensure_folder_exists(output_path)
        get_mi_json(wp, url, output_path)

# Overview of urls from which no info could be retrieved: 
log_regex = re.compile(r'^(.*?) - (.*?) - (.*?) - (.*?) - (.*)$')
log_data = []
with open('generate_input.log', 'r') as file:
    for line in file:
        match = log_regex.match(line.strip())
        if match:
            timestamp, level, wp, url, message = match.groups()
            log_data.append({'Timestamp': timestamp, 'Level': level, 'WP': wp, 'URL':url, 'Message': message})

df_log = pd.DataFrame(log_data)
print(df_log.head())
print(df_log.columns)
df_log.to_csv('input/urls_to_manually_check.csv', index=False)


###### Notes on manually checked urls ######
# doi urls:
# https://www.vliz.be/nl/imis?dasid=4687&doiid=763&show=json 
# https://www.vliz.be/en/imis?dasid=4687&doiid=618&show=json --> same dataset with different DOIs!
# https://www.vliz.be/en/imis?dasid=4688&doiid=619&show=json
#get_mi_json('https://www.vliz.be/en/imis?dasid=4687', './input/WP3_json')
#get_mi_json('https://www.vliz.be/en/imis?dasid=4687', './input/WP3_json')
#get_mi_json('https://www.vliz.be/en/imis?dasid=4688', './input/WP3_json')

## other urls
# https://rshiny.lifewatch.be/zooscan-data/   
# --> no clear metadata download

# https://obis.org/dataset/afa5b0e8-826d-4433-b698-beb176ef7880    
# --> https://www.eurobis.org//imis?dasid=4687
# --> json data already in /input/WP3_json with doi_url

# https://geonode.goosocean.org/layers/geonode_data:geonode:zooplankton_observations_in_tea_lifewatch_observatory_data 
# --> https://geonode.goosocean.org/layers/geonode:zooplankton_observations_in_tea_lifewatch_observatory_data/metadata_detail
# --> in /input/WP3_text with manual download
# --> metadata of publication not dataset?

# https://rshiny.lifewatch.be/flowcam-data/
# --> no clear metadata download

# https://obis.org/dataset/956d618f-91dc-4930-a253-cdf80ddb9371
# --> https://www.eurobis.org//imis?dasid=4688
# --> json data already in /input/WP3_json with doi_url

# https://geonode.goosocean.org/layers/geonode_data:geonode:phytoplankton_observations_inea_lifewatch_obs
# --> https://geonode.goosocean.org/layers/geonode:phytoplankton_observations_inea_lifewatch_obs/metadata_detail
# --> in /input/WP3_text with manual download
# --> metadata of publication not dataset?

# https://emodnet.ec.europa.eu/geoviewer/?layers=12701:1:1,12548:1:1,11952:1:1,12614:1:1,10538:1:1&basemap=ebwbl&active=undefined&bounds=6.892904534994003,32.576939923538475,49.77985542488438,58.40925855707822&filters=
# --> redirect to general page ...

# https://www.elbe-datenportal.de/FisFggElbe/ausgabe/dbe_gast_20240424_{}.xls
# --> available as xls
# --> url results in download of excel file
# --> no semantic information of columns, hence cannot turn into rdf (json-ld, ttl) with template