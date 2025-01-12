# The MARCO-BOLO Dataset Catalogue

As the MARCO-BOLO (MBO) consortium gathers and produces (meta)data across its work packages (WPs), we'll be building an index of its datasets in this repository. 

To do so, we'll be using the conventions of the IOC-UNESCO [Ocean Data and Information System (ODIS)]([url](https://oceaninfohub.org/odis/)) to ensure that this catalogue's contents are interoperable more globally, and in line with the [Data and Information Strategy]([url](https://unesdoc.unesco.org/ark:/48223/pf0000385542?posInSet=1&queryId=fc0616d9-8a41-42ff-bc0f-1d7ef4355f1a)) of the [UN Decade of Ocean Science for Sustainable Development]([url](https://oceandecade.org/)). 

Further, ODIS alignment will secure discoverability in the [Ocean InfoHub]([url](https://oceaninfohub.org/)) system, and other systems leveraging ODIS, while aligning with the Cross-domain Interoperability Framework (CDIF) being developed through [WorldFAIR](https://worldfair-project.eu/).

Dataset validation reports are available at <https://lab.marcobolo-project.eu/dataset-catalogue/>.

## Datasets metadata gathering procedure

We are still working out the details of gathering the metadata for the described datasets. Our working version of this template, which has some example entries in it, can be found on https://docs.google.com/spreadsheets/d/1Wmjpvj4FI8RK926RU3XsM8yDyKGG53PLZFhfiugIRSk/edit#gid=0, which is on the MBO WP1 training materials googledrive. This version contains the dataset description metadata to be included in the OceanInfoHub json files, it does not also include the provenance metadata.

## Updating JSON-LD Output

This workflow assumes the working directory is `scripts/tests`.

### 1. Download the Latest Spreadsheets
Use [scripts/tests/g_download.py](scripts/tests/g_download.py) to download the latest version of Google Sheets, which lists the MBO datasets for each work package (WP).  
- **Files updated**:  
  - `./input/MARCO-BOLO_Metadata_Dataset_Record_description_*.csv`  
  - `./input/MARCO-BOLO_Metadata_Dataset_Record_agent_*.csv`  

### 2. Generate Metadata Input
Run [scripts/tests/generate_input.py](scripts/tests/generate_input.py) to retrieve metadata records for datasets that have retrievable metadata.  
- **Files updated**:  
  - Metadata records in `./input/WP*/json/*`  

### 3. Generate JSON-LD Output
Run [scripts/tests/generate_output.py](scripts/tests/generate_output.py) to create JSON-LD for each dataset:  
- Based on metadata from the Google Sheet.  
- For datasets with retrievable metadata, additional JSON-LD is generated based on the retrieved metadata.  
- **Files updated**:  
  - JSON-LD files in `./output/WP*/`

