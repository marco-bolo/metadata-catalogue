import pandas as pd
from pathlib import Path
import requests
import json
from urllib.parse import urlparse

def flatten_and_split(input_list):
    result = []
    for sublist in input_list:
        # Convert the sublist item to string and split by '|'
        result.extend(str(sublist).split('|'))
    # Strip whitespace from each resulting part
    result = [item.strip() for item in result]
    return result


def get_mi_json(url:str, output_path:str) -> None:
    
    """
    1.contructs marineinfo-url based on dasid (which follows 'module=dataset&dasid=' in the url)
    2.retrieves the json record from the marineinfo-url 
    3.writes it to a file
    """

    base = urlparse(url).netloc.split('.')[-2]
    dasid = url.split("=")[-1]
    mi_url = f"http://marineinfo.org/id/dataset/{dasid}.json"
    response = requests.get(mi_url)
    if response.status_code == 200:
        data = response.json()
        file_path = f'{output_path}/{base}_{dasid}.json'
        
        with open(file_path, 'w') as json_file:
            json.dump(data, json_file, indent=4)
        
        #print(f"Data successfully saved to {file_path}")
    else:
        #print(f"Failed to retrieve data. HTTP Status code: {response.status_code}")
        pass


## Analyse datasets
files = list(Path('./input/').glob('MARCO-BOLO_Metadata_Dataset_Record_*_Description.csv'))
urls_to_manual_check = []
for wp_file in files:
    df = pd.read_csv(wp_file)
    
    wp_urls = flatten_and_split(list(df.DataLandingPageURL))
    for url in wp_urls:
        if isinstance(url, str) and 'module=dataset&dasid=' in url:
            if 'WP5' in str(wp_file):
                get_mi_json(url, './input/WP5_json')
            if 'WP3' in str(wp_file):
                get_mi_json(url, './input/WP3_json')
        
        else:
            urls_to_manual_check.append(url)
            print(url)

# Convert the list to a DataFrame
df = pd.DataFrame(urls_to_manual_check, columns=['url'])
# Write the DataFrame to a CSV file
df.to_csv("./input/urls_to_manual_check.csv", index=False, header=False)


# doi urls:
# https://www.vliz.be/nl/imis?dasid=4687&doiid=763&show=json 
# https://www.vliz.be/en/imis?dasid=4687&doiid=618&show=json --> same dataset with different DOIs!
# https://www.vliz.be/en/imis?dasid=4688&doiid=619&show=json
get_mi_json('https://www.vliz.be/en/imis?dasid=4687', './input/WP3_json')
get_mi_json('https://www.vliz.be/en/imis?dasid=4687', './input/WP3_json')
get_mi_json('https://www.vliz.be/en/imis?dasid=4688', './input/WP3_json')

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