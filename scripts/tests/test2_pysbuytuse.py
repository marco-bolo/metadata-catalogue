import pandas as pd
import os
from pathlib import Path
from pysubyt import JinjaBasedGenerator, Source, SourceFactory, Settings, Sink, SinkFactory
import json 
from typing import Dict

# Directory containing the json files
directory = Path('scripts/tests/input/')
files = [f for f in directory.iterdir() if f.is_file()]

base_path = Path(".")
tpl_path = base_path
out_path = base_path

name: str = "dataset-template.json.ldt.j2"
generator_settings=Settings.load_from_modifiers("it")

g = JinjaBasedGenerator(str(tpl_path))

for file_path in files:
    try:
        #with open(file_path, 'r') as f:
        #    data = json.load(f)
        #print(data)
        inputs: Dict[str, Source] = {
            "_": SourceFactory.make_source(file_path)
        }_ 
        sink: Sink = SinkFactory.make_sink(outpath / file_Path.stem + ".jsonld")

        
        g.process(
                name,
                inputs,
                generator_settings,
                sink,
                vars_dict={"my_domain": "realexample.org"},
            )

    except FileNotFoundError:
        print(f"The file {file_path} does not exist.")
    except json.JSONDecodeError:
        print(f"Error decoding JSON from the file {file_path}.")