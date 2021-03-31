# OpenSAFELY Service Restoration Observatory (SRO) Template

This is a template repository for making new OpenSAFELY SRO resarch projects.

# About the OpenSAFELY framework

The OpenSAFELY framework is a secure analytics platform for
electronic health records research in the NHS.

Instead of requesting access for slices of patient data and
transporting them elsewhere for analysis, the framework supports
developing analytics against dummy data, and then running against the
real data *within the same infrastructure that the data is stored*.
Read more at [OpenSAFELY.org](https://opensafely.org).

# OpenSAFELY SRO

The aim of the OpenSAFELY SRO is to describe trends and variation in 
clinical activity codes to evaluate NHS service restoration during the 
COVID-19 pandemic.

Variation in ten key indicators of service disruption can be seen 
[in this repo](). 

This template provides the means to explore variation in any clinical
activity codes of interest.

# How to use this template

1. Create a new repository in the OpenSAFELY organisation and select 
sro-template as a template.
2.  Create or select codelist on [OpenSAFELY Codelists](https://codelists.opensafely.org/).
Instructions on how to do this can be found [in this documentation](https://docs.opensafely.org/en/latest/codelist-creation/)
4.  [Add the codelist to your project](https://docs.opensafely.org/en/latest/codelist-project/).
5.  Make changes to config.py in analysis folder.
6.  Update --index-date-range in project.yaml.
7.  Run


