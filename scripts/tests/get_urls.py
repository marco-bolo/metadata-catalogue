import pandas as pd
import os
import requests
import json

def get_mi_json(mi_urls:list, output_path:str) -> None:
    
    for base_url in mi_urls:
        dasid = base_url.split("=")[-1]
        url = f"http://marineinfo.org/id/dataset/{dasid}.json"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            file_path = f'{output_path}/{dasid}.json'
            
            with open(file_path, 'w') as json_file:
                json.dump(data, json_file, indent=4)
            
            print(f"Data successfully saved to {file_path}")
        else:
            print(f"Failed to retrieve data. HTTP Status code: {response.status_code}")

# WP5
WP5_dataset_description = 'scripts/tests/input/MBO_WP5_dataset_description.csv'
df = pd.read_csv(WP5_dataset_description)
WP5_mi_urls = [url for url in df['DataLandingPageURL'].dropna() if url.startswith('http')]
get_mi_json(WP5_mi_urls, 'scripts/tests/input/WP5_json')

# WP3
WP5_dataset_description = 'scripts/tests/input/MBO_WP3_dataset_description.csv'
df = pd.read_csv(WP5_dataset_description)


mi_urls = []
doi_urls = []

flattened_list = []
for url in df.DataLandingPageURL:
    if isinstance(url, str) :
        if '|' in url:
            flattened_list += url.split(' | ')
        else:
            flattened_list.append(url)

for url in flattened_list:
    if '?module=dataset&dasid=' in url:
        mi_urls.append(url) # mi urls
    elif 'doi' in url:
        doi_urls.append(url) # doi urls
    else:
        print(url) #other urls


# mi urls
get_mi_json(mi_urls, 'scripts/tests/input/WP3_json')

# doi urls:
# https://www.vliz.be/nl/imis?dasid=4687&doiid=763&show=json 
# https://www.vliz.be/en/imis?dasid=4687&doiid=618&show=json --> same dataset with different DOIs!
# https://www.vliz.be/en/imis?dasid=4688&doiid=619&show=json
doi_mi_urls = ['https://www.vliz.be/nl/imis?dasid=4687',
               'https://www.vliz.be/en/imis?dasid=4687',
               'https://www.vliz.be/en/imis?dasid=4688'
               ]
get_mi_json(doi_mi_urls, 'scripts/tests/input/WP3_json')

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