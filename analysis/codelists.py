from cohortextractor import codelist_from_csv

codelist = codelist_from_csv("codelists/opensafely-structured-medication-review-nhs-england.csv",
                              system="snomed",
                              column="code",)
