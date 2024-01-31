import os
import rdflib
from pyshacl import validate
import json
from jinja2 import Environment, FileSystemLoader
from datetime import datetime
from pyld import jsonld
from rdflib.plugins.sparql import prepareQuery


DATASET_FOLDERS = ["datasets", "datasets-sandbox"]
REPO_URL = "https://github.com/marco-bolo/dataset-catalogue"
REPO_URL_RAW = "https://raw.githubusercontent.com/marco-bolo/dataset-catalogue"

shape_graph = rdflib.Graph()
shape_graph.parse("validation/shacl/dataset-shape.ttl", format="turtle")


def validate_json(jsonld: str):
    try:
        json.loads(jsonld)
    except ValueError as err:
        return False, None
    return True, None


def validate_rdf(jsonld: str) -> tuple[bool, rdflib.Graph, rdflib.Graph]:
    dataset_graph = rdflib.Graph()
    dataset_graph.parse(data=jsonld, format="json-ld")
    conforms, results_graph, results_text = validate(dataset_graph, shacl_graph=shape_graph, inference="rdfs")

    if conforms:
        return True, None, dataset_graph
    else:
        return False, results_graph, dataset_graph


def get_dataset_files() -> list:
    dataset_files = []
    for dataset_folder in DATASET_FOLDERS:
        for root, dirs, files in os.walk(dataset_folder):
            for file in files:
                if file.endswith(".json") or file.endswith(".jsonld"):
                    dataset_files.append(os.path.join(root, file))
    return dataset_files


def validate_datasets() -> dict:
    dataset_files = get_dataset_files()

    context = {
        "time": datetime.now(),
        "datasets": []
    }

    for dataset_filename in dataset_files:

        dataset_file = open(dataset_filename, "r")
        doc = dataset_file.read()
        dataset_file.close()

        dataset = {
            "filename": dataset_filename,
            "document_url": f"{REPO_URL}/blob/main/{dataset_filename}",
            "document_url_raw": f"{REPO_URL_RAW}/main/{dataset_filename}",
            "rdf_results": {}
        }

        json_ok, json_results = validate_json(doc)
        dataset["json_valid"] = json_ok

        if json_ok:
            framed = jsonld.frame(json.loads(doc), {
                "@context": {},
                "@type": "http://schema.org/Dataset"
            })
            rdf_ok, rdf_results, dataset_graph = validate_rdf(json.dumps(framed))
            dataset["rdf_valid"] = rdf_ok

        if rdf_ok:
            from rdflib import Namespace
            schema = Namespace("http://schema.org/")
            query = prepareQuery("""
                SELECT ?name
                WHERE {
                ?dataset a schema:Dataset ;
                        schema:name ?name .
                }
            """, initNs={"schema": "http://schema.org/"})
            res = dataset_graph.query(query)
            for row in res:
                dataset["name"] = row[0].toPython()
                break

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

context = validate_datasets()
datasets_template = environment.get_template("datasets_template.html")
sitemap_template = environment.get_template("sitemap_template.xml")

with open("docs/_includes/datasets.html", mode="w", encoding="utf-8") as html_file:
    html_file.write(datasets_template.render(context))

with open("docs/sitemap.xml", mode="w", encoding="utf-8") as xml_file:
    xml_file.write(sitemap_template.render(context))
