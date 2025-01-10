"""
Example of running pysubyt as a python library.
This examples uses the it mode to generate a single .jsonld from a single .json file.
Run this script from 'dataset-catalogue/scripts/tests'
"""

import logging
from pysubyt.subyt import Subyt
from pathlib import Path

logging.basicConfig(level=logging.INFO)

# set Workpackages
wps = ['WP2', 'WP3', 'WP4', 'WP5']


# turning retrieved json records into json-ld
# for wp in wps:
#    input_folder = Path(f'./input/{wp}_json')
#    output_folder = Path(f'/output/{wp}_jsonld')
#
#    for file in input_folder.iterdir():
#        subyt_jsonrecord = Subyt(
#            extra_sources={"_": f"./{input_folder}/{file.name}"},
#            sink=f"./{output_folder}/{file.stem}.jsonld",
#            template_name="bioship.jsonld.ldt.j2",
#            template_folder="./templates/",
#            mode="it",
#        )
#        subyt_jsonrecord.process()

# turning record information from spreadsheet into json-ld
for wp in wps:
    output_folder = Path(f'/output/{wp}_jsonld')
    subyt_sheet = Subyt(
        extra_sources={
            "_": f'./input/MARCO-BOLO_Metadata_Dataset_Record_description_{wp}.csv',
            "agents": f'./input/MARCO-BOLO_Metadata_Dataset_Record_agent_{wp}.csv'
            },
        sink="./output/sheet_data/test_{DatasetIdentifier}.jsonld",
        template_name="dataset-template.json.ldt.j2",
        template_folder="./templates/",
    )
    subyt_sheet.process()
