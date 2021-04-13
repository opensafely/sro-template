from cohortextractor import codelist_from_csv

codelist = codelist_from_csv("codelists/opensafely-structured-medication-review-nhs-england.csv",
                              system="snomed",
                              column="code",)



ethnicity_codes = codelist_from_csv(
        "codelists/opensafely-ethnicity.csv",
        system="ctv3",
        column="Code",
        category_column="Grouping_6",
    )