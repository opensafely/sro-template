# Import functions
import pandas as pd
from cohortextractor import StudyDefinition, patients, codelist, Measure
from codelists import codelist, ld_codes
from config import start_date, end_date, codelist_path, demographics

# Get codes from codelist to use in expectations
codelist_df = pd.read_csv(codelist_path)
codelist_expectation_codes = codelist_df["code"].unique()

# Specifiy study defeinition
study = StudyDefinition(
    index_date=start_date,
    # Configure the expectations framework
    default_expectations={
        "date": {"earliest": start_date, "latest": end_date},
        "rate": "exponential_increase",
        "incidence": 0.1,
    },
    population=patients.satisfying(
        """
        registered AND
        (NOT died) AND
        (sex = 'F' OR sex='M') AND
        (age_band != 'missing')
        """,
        registered=patients.registered_as_of(
            "index_date",
            return_expectations={"incidence": 0.9},
        ),
        died=patients.died_from_any_cause(
            on_or_before="index_date",
            returning="binary_flag",
            return_expectations={"incidence": 0.1},
        ),
    ),
    age=patients.age_as_of(
        "index_date",
        return_expectations={
            "rate": "universal",
            "int": {"distribution": "population_ages"},
        },
    ),
    age_band=patients.categorised_as(
        {
            "missing": "DEFAULT",
            "0-19": """ age >= 0 AND age < 20""",
            "20-29": """ age >=  20 AND age < 30""",
            "30-39": """ age >=  30 AND age < 40""",
            "40-49": """ age >=  40 AND age < 50""",
            "50-59": """ age >=  50 AND age < 60""",
            "60-69": """ age >=  60 AND age < 70""",
            "70-79": """ age >=  70 AND age < 80""",
            "80+": """ age >=  80 AND age < 120""",
        },
        return_expectations={
            "rate": "universal",
            "category": {
                "ratios": {
                    "0-19": 0.125,
                    "20-29": 0.125,
                    "30-39": 0.125,
                    "40-49": 0.125,
                    "50-59": 0.125,
                    "60-69": 0.125,
                    "70-79": 0.125,
                    "80+": 0.125,
                }
            },
        },
    ),
    sex=patients.sex(
        return_expectations={
            "rate": "universal",
            "category": {"ratios": {"M": 0.5, "F": 0.5}},
        }
    ),
    practice=patients.registered_practice_as_of(
        "index_date",
        returning="pseudo_id",
        return_expectations={
            "int": {"distribution": "normal", "mean": 25, "stddev": 5},
            "incidence": 0.5,
        },
    ),
    region=patients.registered_practice_as_of(
        "index_date",
        returning="nuts1_region_name",
        return_expectations={
            "category": {
                "ratios": {
                    "North East": 0.1,
                    "North West": 0.1,
                    "Yorkshire and the Humber": 0.1,
                    "East Midlands": 0.1,
                    "West Midlands": 0.1,
                    "East of England": 0.1,
                    "London": 0.2,
                    "South East": 0.2,
                }
            }
        },
    ),
    imd=patients.categorised_as(
        {
            "0": "DEFAULT",
            "1": """index_of_multiple_deprivation >=1 AND index_of_multiple_deprivation < 32844*1/5""",
            "2": """index_of_multiple_deprivation >= 32844*1/5 AND index_of_multiple_deprivation < 32844*2/5""",
            "3": """index_of_multiple_deprivation >= 32844*2/5 AND index_of_multiple_deprivation < 32844*3/5""",
            "4": """index_of_multiple_deprivation >= 32844*3/5 AND index_of_multiple_deprivation < 32844*4/5""",
            "5": """index_of_multiple_deprivation >= 32844*4/5 AND index_of_multiple_deprivation < 32844""",
        },
        index_of_multiple_deprivation=patients.address_as_of(
            "index_date",
            returning="index_of_multiple_deprivation",
            round_to_nearest=100,
        ),
        return_expectations={
            "rate": "universal",
            "category": {
                "ratios": {
                    "0": 0.05,
                    "1": 0.19,
                    "2": 0.19,
                    "3": 0.19,
                    "4": 0.19,
                    "5": 0.19,
                }
            },
        },
    ),
    learning_disability=patients.categorised_as(
        {
            "missing": "DEFAULT",
            "Record of learning disability": """ ld = 1 """,
            "No record of learning disability": """ ld=0 """,
        },
        ld=patients.with_these_clinical_events(
            ld_codes,
            on_or_before="index_date",
            returning="binary_flag",
            return_expectations={
                "incidence": 0.01,
            },
        ),
        return_expectations={
            "rate": "universal",
            "category": {
                "ratios": {
                    "Record of learning disability": 0.1,
                    "No record of learning disability": 0.9,
                }
            },
        },
    ),
    care_home_status=patients.care_home_status_as_of(
        "index_date",
        categorised_as={
            "CareHome": """
              IsPotentialCareHome
              AND LocationDoesNotRequireNursing='Y'
              AND LocationRequiresNursing='N'
            """,
            "NursingHome": """
              IsPotentialCareHome
              AND LocationDoesNotRequireNursing='N'
              AND LocationRequiresNursing='Y'
            """,
            "CareOrNursingHome": "IsPotentialCareHome",
            "PrivateHome": "NOT IsPotentialCareHome",
            "": "DEFAULT",
        },
        return_expectations={
            "rate": "universal",
            "category": {
                "ratios": {
                    "CareHome": 0.30,
                    "NursingHome": 0.10,
                    "CareOrNursingHome": 0.10,
                    "PrivateHome": 0.45,
                    "": 0.05,
                },
            },
        },
    ),
    event=patients.with_these_clinical_events(
        codelist=codelist,
        between=["index_date", "last_day_of_month(index_date)"],
        returning="binary_flag",
        return_expectations={"incidence": 0.5},
    ),
    event_code=patients.with_these_clinical_events(
        codelist=codelist,
        between=["index_date", "last_day_of_month(index_date)"],
        returning="code",
        return_expectations={
            "category": {
                "ratios": {
                    x: 1 / len(codelist_expectation_codes)
                    for x in codelist_expectation_codes
                }
            },
        },
    ),
)

# Create default measures
measures = [
    # events broken down by code
    Measure(
        id="event_code_rate",
        numerator="event",
        denominator="population",
        group_by=["event_code"],
        small_number_suppression=False,
    ),
    # events broken down by practice
    Measure(
        id="practice_rate",
        numerator="event",
        denominator="population",
        group_by=["practice"],
        small_number_suppression=False,
    ),
    # population rate
    Measure(
        id="population_rate",
        numerator="event",
        denominator="population",
        group_by="population",
        small_number_suppression=False,
    ),
]


# Add demographics measures

for d in demographics:
    m = Measure(
        id=f"{d}_rate",
        numerator="event",
        denominator="population",
        group_by=[d],
        small_number_suppression=False,
    )
    measures.append(m)
