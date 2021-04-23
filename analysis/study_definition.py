
# Import functions
import json
import pandas as pd

from cohortextractor import (
    StudyDefinition, 
    patients, 
    codelist, 
    Measure,
    codelist_from_csv
)

# Import codelists
from codelists import codelist, ld_codes

from config import start_date, end_date, demographics, codelist_code_column, codelist_path

codelist_df = pd.read_csv(codelist_path)
codelist_expectation_codes = codelist_df[codelist_code_column].unique()[0]


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
            "0": "DEFAULT",
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
                    "0": 0.001,
                    "0-19": 0.124,
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
    
    imd=patients.address_as_of(
        "index_date",
        returning="index_of_multiple_deprivation",
        round_to_nearest=100,
        return_expectations={
            "rate": "universal",
            "category": {"ratios": {"100": 0.2, "200": 0.2, "300": 0.2, "400": 0.2, "500": 0.2}},
        },
    ),

    learning_disability=patients.with_these_clinical_events(
        ld_codes,
        on_or_before="index_date",
        returning="binary_flag",
        return_expectations={"incidence": 0.01, },
    ),


    event =patients.with_these_clinical_events(
        codelist=codelist,
        between=["index_date", "last_day_of_month(index_date)"],
        returning="binary_flag",
        return_expectations={"incidence": 0.5}
    ),

    event_code=patients.with_these_clinical_events(
        codelist=codelist,
        between=["index_date", "last_day_of_month(index_date)"],
        returning="code",
        return_expectations={"category": {
            "ratios": {codelist_expectation_codes: 1}}, }
    ),
    
)

# Create default measures
measures = [

    Measure(
        id="total",
        numerator="event",
        denominator="population",
        group_by=["age_band"]
    ),

    Measure(
        id="event_code",
        numerator="event",
        denominator="population",
        group_by=["age_band","event_code"]
    ),

    Measure(
        id="practice",
        numerator="event",
        denominator="population",
        group_by=["age_band","practice"]
    ),



]


#Add demographics measures

for d in demographics:

    if d=='age_band':
        m = Measure(
        id=d,
        numerator="event",
        denominator="population",
        group_by=["age_band"]
    )
        measures.append(m)
    elif d=="ethnicity":
        pass

   
    else:

        m = Measure(
            id=d,
            numerator="event",
            denominator="population",
            group_by=["age_band", d]
        )
        measures.append(m)


