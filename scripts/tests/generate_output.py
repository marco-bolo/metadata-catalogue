"""
This script:
1. processes metadata from Google Spreadsheets of MBO WP and generates JSON-LD files for each dataset.
2. additionally, processes dataset-specific JSON metadata records for datasets with retrievable metadata, generating corresponding JSON-LD files.
"""

import logging
from pysubyt.subyt import Subyt
from pathlib import Path
import json_repair
import json
import os

logging.basicConfig(level=logging.INFO)
repair = True

# set Workpackages

wps = [
    'WP2',
    'WP3',
    # 'WP4',  # pysubyt fails on empty CSV
    'WP5'
]

# triplize dataset metadata from g-spreadsheet of each WP

for wp in wps:
    output_path = f"./output/{wp}"
    subyt_sheet = Subyt(
        extra_sources={
            "_": f'./input/MARCO-BOLO_Metadata_Dataset_Record_description_{wp}.csv',
            "agents": f'./input/MARCO-BOLO_Metadata_Dataset_Record_agent_{wp}.csv'
            },
        sink=f"{output_path}/{{DatasetIdentifier}}.jsonld",
        template_name="gsheet.jsonld.ldt.j2",
        template_folder="./templates/",
    )
    subyt_sheet.process()

    # repair JSON-LD files

    if repair:
        jsonld_files = [os.path.join(output_path, f) for f in os.listdir(output_path) if f.endswith(".jsonld")]
        for jsonld_file in jsonld_files:
            try:
                with open(jsonld_file, "r") as input_file:
                    fixed = json_repair.load(input_file)
                with open(jsonld_file, "w") as output_file:
                    output_file.write(json.dumps(fixed, indent=4))
            except Exception as e:
                logging.error(f"Failed to fix {jsonld_file}: {e}")

# triplize metadata record of datasets with retrievable metadata record

for wp in wps:
    input_folder = Path(f'./input/{wp}/json')
    output_folder = Path(f'/output/{wp}')
    for file in input_folder.iterdir():
        sink = f"./output/{wp}/{file.stem}_metadatarecord.jsonld"
        subyt_jsonrecord = Subyt(
            extra_sources={
                "_": f"./{input_folder}/{file.name}",
                },
            sink=sink,
            template_name="bioship.jsonld.ldt.j2",
            template_folder="./templates/",
            mode="it",
        )
        subyt_jsonrecord.process()
