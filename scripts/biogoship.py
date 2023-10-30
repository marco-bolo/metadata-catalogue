# This script reads supplementary data from https://www.nature.com/articles/s41597-021-00889-9
# to generate a metadata graph for the Bio-GO-SHIP cruises.

import pandas as pd
import requests
from shapely.geometry import LineString
from shapely import wkt
from skimpy import clean_columns
import json
import os
from io import BytesIO
import shapely
import re


DATASET_FOLDER = "datasets/biogoship"


def create_project() -> dict:
    return {
        "@id": "https://biogoship.org",
        "@type": "ResearchProject",
        "identifier": "https://biogoship.org",
        "description": "Bio-GO-SHIP aims to become an international collaboration to measure, understand, and predict the distribution and biogeochemical role of pelagic plankton communities. The project leverages the global-reaching GO-SHIP platform and its complementary hydrographic measurements.",
        "name": "Bio-GO-SHIP",
        "url": "https://biogoship.org",
        "areaServed": {
            "@type": "Country",
            "name": "Global"
        },
        "parentOrganization": {
            "@type": "Organization",
            "@id": "https://www.go-ship.org",
            "name": "GO-SHIP"
        },
        "funding": {
            "@type": "Grant",
                "funder": {
                "@type": "Organization",
                "name": "National Oceanographic Partnership Program"
            }
        }
    }


def create_dataset() -> dict:
    return {
        "@id": "https://www.ebi.ac.uk/ena/browser/view/PRJNA656268",
        "@type": "Dataset",
        "identifier": "https://www.ebi.ac.uk/ena/browser/view/PRJNA656268",
        "name": "Bio-GO-SHIP: Global marine 'omics studies of repeat hydrography transects",
        "description": "Bio-GO-SHIP: Global marine 'omics studies of repeat hydrography transects",
        "url": "https://www.ebi.ac.uk/ena/browser/view/PRJNA656268",
        "author": {
            "@id": "https://biogoship.org",
        },
        "includedInDataCatalog": {
            "@id": "https://www.ebi.ac.uk/ena",
            "@type": "DataCatalog",
        },
        "variableMeasured": {
            "@type": "PropertyValue",
            "@id": "http://purl.obolibrary.org/obo/PCO_1000004",
            "name": "Microbial community composition",
            "measurementMethod": {
                "@id": "https://doi.org/10.1038/s41597-021-00889-9"
            }
        },
        "distribution": [
            {
                "@type": "DataDownload",
                "contentUrl": "https://www.ebi.ac.uk/ena/browser/view/PRJNA656268",
                "encodingFormat": "https://maq.sourceforge.net/fastq.shtml"
            }
        ],
        "about": [
            {
                "@id": "https://www.goosocean.org/eov/microbial_biomass_diversity",
                "@type": "https://www.goosocean.org/eov",
                "name": "Microbial biomass and diversity EOV"
            }
        ]
    }


def create_linestring(s: str) -> str:
    return wkt.dumps(LineString(zip(s["longitude_decimal_deg_w"], s["latitude_decimal_deg_n"])))


def row_to_document(row: pd.Series) -> dict:
    document = {
        "@id": f"https://biogoship.org/cruise/{row['section_id']}",
        "@type": "Event",
        "name": row["section_id"],
        "startDate": row["min_date"],
        "endDate": row["max_date"],
        "description": f"Bio-GO-SHIP cruise {row['ccdho_expocode'] if row['ccdho_expocode'] else '(unknown)'} section {row['section_id']}",
        "organizer": {
            "@id": "https://biogoship.org"
        },
        "geosparql:hasGeometry": {
            "@type": "http://www.opengis.net/ont/sf#Geometry",
            "geosparql:asWKT": {
                "@type": "http://www.opengis.net/ont/geosparql#wktLiteral",
                "@value": row["wkt"]
            },
            "geosparql:crs": {
                "@id": "http://www.opengis.net/def/crs/OGC/1.3/CRS84"
            }
        }
    }
    if row["ccdho_expocode"]:
        document["identifier"] = row["ccdho_expocode"]
        document["url"] = f"https://cchdo.ucsd.edu/cruise/{row['ccdho_expocode']}"
    return document    


def create_cruises() -> list[dict]:
    url = "https://static-content.springer.com/esm/art%3A10.1038%2Fs41597-021-00889-9/MediaObjects/41597_2021_889_MOESM1_ESM.xlsx"

    response = requests.get(url)
    content = response.content
    samples = clean_columns(pd.read_excel(BytesIO(content), engine="openpyxl"))

    df = samples.fillna("").groupby(["section_id", "ccdho_expocode"]).apply(lambda s: pd.Series({ 
        "min_year": s["year"].min(),
        "max_year": s["year"].max(),
        "min_date": s["iso_date_time_utc"].min(),
        "max_date": s["iso_date_time_utc"].max(),
        "wkt": create_linestring(s)
    })).reset_index()

    return df.apply(row_to_document, axis=1).tolist()


def create_graph() -> dict:
    project = create_project()
    dataset = create_dataset()
    cruises = create_cruises()

    # add cruises to dataset about

    for cruise in cruises:
        dataset["about"].append({
            "@id": cruise["@id"]
        })

    # calculate dataset spatial coverage

    geometries = [shapely.wkt.loads(cruise["geosparql:hasGeometry"]["geosparql:asWKT"]["@value"]) for cruise in cruises]
    bbox_wkt = str(shapely.box(*shapely.bounds(shapely.union_all(geometries))))
    bbox_coords = re.search("\(\((.*)\)\)", bbox_wkt).group(1)
    dataset["spatialCoverage"] = {
        "@type": "Place",
        "geo": {
            "@type": "GeoShape",
            "polygon": bbox_coords
        }
    }
    dataset["hasGeometry"] = {
        "@type": "http://www.opengis.net/ont/sf#Geometry",
        "geosparql:asWKT": {
            "@type": "http://www.opengis.net/ont/geosparql#wktLiteral",
            "@value": bbox_wkt
        },
        "geosparql:crs": {
            "@id": "http://www.opengis.net/def/crs/OGC/1.3/CRS84"
        }
    }

    return {
        "@context": {
            "@vocab": "https://schema.org/",
            "geosparql": "http://www.opengis.net/ont/geosparql#"
        },
        "@graph": [
            project,
            dataset,
            *cruises
        ]
    }


if not os.path.exists(os.path.expanduser(DATASET_FOLDER)):
    os.makedirs(os.path.expanduser(DATASET_FOLDER))

with open(os.path.expanduser(f"{DATASET_FOLDER}/biogoship.json"), "w") as outfile:
    graph = create_graph()
    outfile.write(json.dumps(graph, indent=4))
