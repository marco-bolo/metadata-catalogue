import os
import rdflib
from pyshacl import validate

shape_graph = rdflib.Graph()
shape_graph.parse("validation/shacl/dataset-shape.ttl", format="turtle")

files = [os.path.join("datasets", f) for f in os.listdir("datasets") if os.path.isfile(os.path.join("datasets", f))]

for f in files:
    print(f)
    dataset_graph = rdflib.Graph()
    dataset_graph.parse(f, format="json-ld")

    conforms, results_graph, results_text = validate(dataset_graph, shacl_graph=shape_graph, inference="rdfs")

    if conforms:
        print("Validation successful")
    else:
        print("Validation failed")
        print(results_text)
