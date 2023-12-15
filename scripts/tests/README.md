This folder contains the test material for the datasets description work.  

The first tests were to collect metadata about datasets via a googlesheet and to then turn that into RDF via a templating approach.  

The (test) googlesheet with some (test) datasets described there can be found on https://docs.google.com/spreadsheets/d/1Wmjpvj4FI8RK926RU3XsM8yDyKGG53PLZFhfiugIRSk/edit#gid=0 . A cleaned-up version of that (e.g. removing the extra rows and comments therein) was used as the test dataset to create the RDF and can be found in ./mbo_dummy_data.

The templating approach makes use of [pysubyt](https://github.com/vliz-be-opsci/pysubyt); and following command was used to create a test-output:

``` linux
pysubyt --input /mbo_dummy_data/Description.csv 
    --templates ./ 
    --name mbo_spreadsheet_template.ttl.j2 
    --set Access /mbo_dummy_data/Access.csv 
    --set Acknowledgements /mbo_dummy_data/Acknowledgements.csv
    --set Agents /mbo_dummy_data/Agents.csv 
    --set Coverage /mbo_dummy_data/Coverage.csv 
    --set Links /mbo_dummy_data/Links.csv 
    --set Projects /mbo_dummy_data/Projects.csv
    --output /test_output/test_{date}.ttl
```