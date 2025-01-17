To hold the templates for describing objects (datasets, software, provenance) that the MBO technical WPs need to use to describe and publish their objects on OIH.
We do not have datasets templates at present as we are using a googlesheet-templatingTojson approach instead.

For dataset-provenance.jsonld: This file is an example of how to document a number of single activities performed on data. This does not include any material processing activites, only digital activities that start from data and produce data.
* someone aquires data from someone else
* someone processes data via some software

What is being documented are the activities performed, *not* the actual objects (the data, the software, the outputs) themselves. 
In real life, more than one activity will happen, e.g. data will be aquired from an archive, quality controled, and then processed. To describe the provenance of these three steps would require a description of one data aquisition and two data processings

