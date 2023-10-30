import os
import rdflib
from pyshacl import validate
import json
from jinja2 import Environment, FileSystemLoader


DATASET_FOLDER = "datasets"
REPO_URL = "https://github.com/marco-bolo/dataset-catalogue"

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
        return False, results_graph


def get_dataset_files() -> list:
    dataset_files = []
    for root, dirs, files in os.walk("datasets"):
        for file in files:
            if file.endswith(".json") or file.endswith(".jsonld"):
                dataset_files.append(os.path.join(root, file))
    return dataset_files


def validate_datasets() -> dict:
    dataset_files = get_dataset_files()

    context = {"datasets": []}

    for dataset_filename in dataset_files:

        dataset_file = open(dataset_filename, "r")
        jsonld = dataset_file.read()
        dataset_file.close()

        json_ok, json_results = validate_json(jsonld)
        if json_ok:
            rdf_ok, rdf_results = validate_rdf(jsonld)

        dataset = {
            "filename": dataset_filename,
            "document_url": f"{REPO_URL}/blob/main/{dataset_filename}",
            "json_valid": json_ok,
            "rdf_valid": rdf_ok,
            "rdf_results": {}
        }

        if not rdf_ok:
            for subject, predicate, obj in rdf_results:
                if subject.toPython() not in dataset["rdf_results"]:
                    dataset["rdf_results"][subject.toPython()] = {}
                if predicate.toPython() == "http://www.w3.org/ns/shacl#resultMessage" or predicate.toPython() == "http://www.w3.org/ns/shacl#resultPath" or predicate.toPython() == "http://www.w3.org/ns/shacl#resultSeverity":
                    dataset["rdf_results"][subject.toPython()][predicate.toPython().replace("http://www.w3.org/ns/shacl#", "")] = obj.toPython()    
            dataset["rdf_results"] = [dataset["rdf_results"][key] for key in dataset["rdf_results"] if len(dataset["rdf_results"][key]) > 0]

        context["datasets"].append(dataset)

    return context


environment = Environment(loader=FileSystemLoader("docs/_includes/"))
template = environment.get_template("datasets_template.html")

with open("docs/_includes/datasets.html", mode="w", encoding="utf-8") as html_file:
    context = validate_datasets()
    html_file.write(template.render(context))
