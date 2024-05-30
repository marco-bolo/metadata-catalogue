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
wps = ['WP3', 'WP5']

for wp in wps: 
    input_folder = Path(f'./input/{wp}_json')
    output_folder = Path(f'/output/{wp}_jsonld')

    for file in input_folder.iterdir():

        subyt = Subyt(
            extra_sources={"_": f"./{input_folder}/{file.name}"},
            sink=f"./{output_folder}/{file.stem}.jsonld",
            template_name="bioship.jsonld.ldt.j2",
            template_folder="./templates/",
            mode="it",
        )
        subyt.process()
