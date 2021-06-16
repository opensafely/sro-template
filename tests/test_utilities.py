import pandas
import pytest
from analysis import utilities
from pandas import testing
import numpy as np


@pytest.fixture
def imd_measure_table_from_csv():
    """
    Returns a measure table that could have been read from a CSV file.
    """
    return pandas.DataFrame(
        {
            "imd": pandas.Series([1, 2, 3, 4, 5, 1, 2, 3, 4, 5]),
            "event": pandas.Series([0, 1, 1, 0, 1, 0, 1, 1, 0, 1]),
            "population": pandas.Series([1, 1, 1, 1, 1, 1, 1, 1, 1, 1]),
            "value": pandas.Series([0, 1, 1, 0, 1, 0, 1, 1, 0, 1]),
            "date": pandas.to_datetime(pandas.Series(
                [
                    "2019-01-01",
                    "2019-01-01",
                    "2019-01-01",
                    "2019-01-01",
                    "2019-01-01",
                    "2019-02-01",
                    "2019-02-01",
                    "2019-02-01",
                    "2019-02-01",
                    "2019-02-01",
                ]
            )),
        }
    )

@pytest.fixture
def measure_table():
    """Returns a measure table that could have been read by calling `load_and_drop`."""
    mt = pandas.DataFrame(
        {
            "group": pandas.Categorical(['A', 'B', 'A', 'B']),
            "event": pandas.Series([1, 6, 3, 7]),
            "population": pandas.Series([10, 10, 10, 10]),
            "value": pandas.Series([1/10, 6/10, 3/10, 7/10]),
            "date": pandas.Series(["2019-01-01", "2019-01-01", "2019-02-01", "2019-02-01"]),
        }
    )
    mt["date"] = pandas.to_datetime(mt["date"])
    return mt

def test_calculate_imd_group(imd_measure_table_from_csv):


    obs = utilities.calculate_imd_group(imd_measure_table_from_csv, 'event', 'value')
    
    exp = pandas.DataFrame(
        {
            "imd": pandas.Categorical(['Most deprived', '2', '3', '4', 'Least deprived', 'Most deprived', '2', '3', '4', 'Least deprived'], ordered=True).reorder_categories(['Most deprived', '2', '3', '4', 'Least deprived']),
            "event": pandas.Series([0, 1, 1, 0, 1, 0, 1, 1, 0, 1]),
            "population": pandas.Series([1, 1, 1, 1, 1, 1, 1, 1, 1, 1]),
            "value": pandas.Series([0, 1, 1, 0, 1, 0, 1, 1, 0, 1]),
            "date": pandas.to_datetime(pandas.Series(
                [
                    "2019-01-01",
                    "2019-01-01",
                    "2019-01-01",
                    "2019-01-01",
                    "2019-01-01",
                    "2019-02-01",
                    "2019-02-01",
                    "2019-02-01",
                    "2019-02-01",
                    "2019-02-01",
                ]
            )),
        }
    )
    testing.assert_frame_equal(obs, exp)

def test_redact_small_numbers(measure_table):
    obs = utilities.redact_small_numbers(measure_table, 5, 'event', 'population', 'value')
    
    exp = pandas.DataFrame(
        {
            # "group": pandas.Categorical(['Most deprived', '2', '3', '4', 'Least deprived', 'Most deprived', '2', '3', '4', 'Least deprived'], ordered=True).reorder_categories(['Most deprived', '2', '3', '4', 'Least deprived']),
            "group": pandas.Categorical(['A', 'B', 'A', 'B']),
            "event": pandas.Series([np.nan, np.nan, np.nan, 7]),
            "population": pandas.Series([10, 10, 10, 10]),
            "value": pandas.Series([np.nan, np.nan, np.nan, 0.7]),
            "date": pandas.to_datetime(pandas.Series(
                [
                    "2019-01-01",
                    "2019-01-01",
                    "2019-02-01",
                    "2019-02-01",
                ]
            )),
        }
    )
    
    testing.assert_frame_equal(obs, exp)