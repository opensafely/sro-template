from cohortextractor import codelist_from_csv
from config import codelist_path


# Change the path of the codelist to your chosen codelist
codelist = codelist_from_csv(codelist_path,
                              system="snomed",
                              column="code",)


ethnicity_codes = codelist_from_csv(
        "codelists/opensafely-ethnicity.csv",
        system="ctv3",
        column="Code",
        category_column="Grouping_6",
    )

ld_codes = codelist_from_csv(
    "codelists/opensafely-learning-disabilities.csv",
    system="ctv3",
    column="CTV3Code",
)