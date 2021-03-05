
# Import functions

from cohortextractor import (
    StudyDefinition, 
    patients, 
    codelist, 
    Measure,
    codelist_from_csv
)

# Import codelists
from codelists import *


start_date = "2020-12-07"
end_date = "2021-02-01"


# Specifiy study defeinition

study = StudyDefinition(
    index_date="2020-12-07",
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
        (age != 'missing')
        """,

        registered=patients.registered_as_of(
            "index_date",
            return_expectations={"incidence": 0.9},
        ),

        died=patients.died_from_any_cause(
            on_or_before="index_date",
            returning="binary_flag",
            return_expectations={"incidence": 0.1}
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
            "0-4": "age >= 0 AND age < 5",
            "5-9": "age >= 5 AND age < 10",
            "10-14": "age >= 10 AND age < 15",
            "15-19": "age >= 15 AND age < 20",
            "20-24": "age >= 20 AND age < 25",
            "25-29": "age >= 25 AND age < 30",
            "30-34": "age >= 30 AND age < 35",
            "35-39": "age >= 35 AND age < 40",
            "40-44": "age >= 40 AND age < 45",
            "45-49": "age >= 45 AND age < 50",
            "50-54": "age >= 50 AND age < 55",
            "55-59": "age >= 55 AND age < 60",
            "60-64": "age >= 60 AND age < 65",
            "65-69": "age >= 65 AND age < 70",
            "70-74": "age >= 70 AND age < 75",
            "75-79": "age >= 75 AND age < 80",
            "80-84": "age >= 80 AND age < 85",
            "85-89": "age >= 85 AND age < 90",
            "90plus": "age >= 90",
            "missing": "DEFAULT",
        },
        return_expectations={
            "rate": "universal",
            "category": {
                "ratios": {
                    "0-4": 0.05,
                    "5-9": 0.05,
                    "10-14": 0.05,
                    "15-19": 0.05,
                    "20-24": 0.05,
                    "25-29": 0.05,
                    "30-34": 0.05,
                    "35-39": 0.05,
                    "40-44": 0.05,
                    "45-49": 0.1,
                    "50-54": 0.05,
                    "55-59": 0.05,
                    "60-64": 0.05,
                    "65-69": 0.05,
                    "70-74": 0.05,
                    "75-79": 0.05,
                    "80-84": 0.05,
                    "85-89": 0.05,
                    "90plus": 0.05,
                    "missing": 0,
                }
            },
        }
    ),


    sex=patients.sex(
        return_expectations={
            "rate": "universal",
            "category": {"ratios": {"M": 0.49, "F": 0.5, "U": 0.01}},
        }
    ),

    practice=patients.registered_practice_as_of(
        "index_date",
        returning="pseudo_id",
        return_expectations={
            "int": {"distribution": "normal", "mean": 25, "stddev": 5}, "incidence": 0.5}
    ),

    region=patients.registered_practice_as_of(
        "index_date",
        returning="nuts1_region_name",
        return_expectations={"category": {"ratios": {
            "North East": 0.1,
            "North West": 0.1,
            "Yorkshire and the Humber": 0.1,
            "East Midlands": 0.1,
            "West Midlands": 0.1,
            "East of England": 0.1,
            "London": 0.2,
            "South East": 0.2, }}}
    ),

    event_x =patients.with_these_clinical_events(
        codelist=holder_codelist,
        between=["index_date", "index_date + 1 month"],
        returning="binary_flag",
        return_expectations={"incidence": 0.5}
    ),

    event_x_event_code=patients.with_these_clinical_events(
        codelist=holder_codelist,
        between=["index_date", "index_date + 1 month"],
        returning="code",
        return_expectations={"category": {
            "ratios": {"1239511000000100": 1}}, }
    ),
    
)


measures = [
   

    Measure(
        id="1_total",
        numerator="event_x",
        denominator="population",
        group_by=["age_band"]
    ),

    Measure(
        id="1_event_code",
        numerator="event_x",
        denominator="population",
        group_by=["age_band","event_x_event_code"]
    ),

    Measure(
        id="1_practice_only",
        numerator="event_x",
        denominator="population",
        group_by=["age_band","practice"]
    ),

    Measure(
        id="1_by_region",
        numerator="event_x",
        denominator="population",
        group_by=["age_band","region"],
    ),

    Measure(
        id="1_by_sex",
        numerator="event_x",
        denominator="population",
        group_by=["age_band","sex"],
    ),

    Measure(
        id="1_by_age_band",
        numerator="event_x",
        denominator="population",
        group_by=["age_band"],
    ),


    
]
