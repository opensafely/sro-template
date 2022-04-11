# OpenSAFELY SRO

The aim of the OpenSAFELY SRO is to describe trends and variation in 
clinical activity codes to evaluate NHS service restoration during the 
COVID-19 pandemic.

Variation in eleven key indicators of service disruption can be seen 
[in this report](https://reports.opensafely.org/reports/sro-measures/). 

This template provides the means to explore variation in any clinical
activity codes of interest.

# OpenSAFELY Service Restoration Observatory (SRO) Template

This is a template repository for making new OpenSAFELY SRO resarch projects.
It allows you to easily generate a report to describe changes in coding trends 
for any codelists available on OpenCodelists.

# How to use this template

1. Create or select codelist on [OpenSAFELY Codelists](https://codelists.opensafely.org/).
Instructions on how to do this can be found [in this documentation](https://docs.opensafely.org/en/latest/codelist-creation/).
2. Create a new repository in the OpenSAFELY organisation and select 
sro-template as a template.
3. [Add your chosen codelist to your project](https://docs.opensafely.org/en/latest/codelist-project/).
4. Specify the parameters for your project in `config.py` in the analysis folder. You can:
  * Set the study start and end date (in the format YYYY--MM-DD). Data for each month between these two dates will be described.
  * Choose a set of key demographic variables by which coding activity will be broken down. The available options are "sex", 
    "age_band", "region", "imd", "ethnicity", "learning_disability" and "care_home_status".
  * Specify the title for your measure. This will be used to populate text within the report.
  * Provide the path to the codelist you added to your project in step 3.
5.  Update the `--index-date-range` in `project.yaml` to match the dates defined in step 4 in the  `generate_study_population` and `generate_study_population_practice_count` actions.
8.  This code can then be [run locally](https://docs.opensafely.org/en/latest/actions-pipelines/#running-your-code-locally) using the command `opensafely run run_all`
9.  For instructions on how to run this code against real data [see this documentation](https://docs.opensafely.org/en/latest/job-server/).
