import os
import rdflib
from pyshacl import validate
import json


shape_graph = rdflib.Graph()
shape_graph.parse("validation/shacl/dataset-shape.ttl", format="turtle")


def validate_json(jsonld: str):
    try:
        json.loads(jsonld)
    except ValueError as err:
        return False, None
    return True, None


def validate_rdf(jsonld: str):
    dataset_graph = rdflib.Graph()
    dataset_graph.parse(data=jsonld, format="json-ld")
    conforms, results_graph, results_text = validate(dataset_graph, shacl_graph=shape_graph, inference="rdfs")

    if conforms:
        return True, None
    else:
        return False, results_text


dataset_files = [os.path.join("datasets", f) for f in os.listdir("datasets") if os.path.isfile(os.path.join("datasets", f))]

for dataset_filename in dataset_files:

    print(dataset_filename)

    dataset_file = open(dataset_filename, "r")
    jsonld = dataset_file.read()
    dataset_file.close()

    json_ok, json_results = validate_json(jsonld)
    if json_ok:
        rdf_ok, rdf_results = validate_rdf(jsonld)
        print(rdf_results)

    print(json_ok, rdf_ok)
