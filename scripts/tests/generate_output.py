"""
This script:
1. processes metadata from Google Spreadsheets of MBO WP and generates JSON-LD files for each dataset.
2. additionally, processes dataset-specific JSON metadata records for datasets with retrievable metadata, generating corresponding JSON-LD files.
"""

import logging
from pysubyt.subyt import Subyt
from pathlib import Path

logging.basicConfig(level=logging.INFO)

# set Workpackages
wps = [
    'WP2',
    'WP3',
    # 'WP4',  # pysubyt fails on empty CSV
    'WP5'
]

# triplize dataset metadata from g-spreadsheet of each WP
for wp in wps: 
    output_folder = Path(f'/output/{wp}_jsonld')
    subyt_sheet = Subyt(
        extra_sources={
            "_": f'./input/MARCO-BOLO_Metadata_Dataset_Record_description_{wp}.csv',
            "agents": f'./input/MARCO-BOLO_Metadata_Dataset_Record_agent_{wp}.csv'
            },
        sink=f"./output/{wp}/{{DatasetIdentifier}}.jsonld",
        template_name="gsheet.jsonld.ldt.j2",
        template_folder="./templates/",
    )
    subyt_sheet.process()

# triplize metadata record of datasets with retrievable metadata record 
for wp in wps: 
    input_folder = Path(f'./input/{wp}/json')
    output_folder = Path(f'/output/{wp}')
    for file in input_folder.iterdir():
        subyt_jsonrecord = Subyt(
            extra_sources={
                "_": f"./{input_folder}/{file.name}",
                },
            sink=f"./output/{wp}/{file.stem}_metadatarecord.jsonld",
            template_name="bioship.jsonld.ldt.j2",
            template_folder="./templates/",
            mode="it",
        )
        subyt_jsonrecord.process()
