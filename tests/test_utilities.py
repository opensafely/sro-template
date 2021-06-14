import pandas
import pytest
from analysis import utilities
from pandas import testing


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
            "date": pandas.Series(
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
            ),
        }
    )


def test_calculate_imd_group(imd_measure_table_from_csv):


    obs = utilities.calculate_imd_group(imd_measure_table_from_csv, 'event', 'value')
    
    exp = pandas.DataFrame(
        {
            "imd": pandas.Categorical(['Most deprived', '2', '3', '4', 'Least deprived', 'Most deprived', '2', '3', '4', 'Least deprived'], ordered=True).reorder_categories(['Most deprived', '2', '3', '4', 'Least deprived']),
            "event": pandas.Series([0, 1, 1, 0, 1, 0, 1, 1, 0, 1]),
            "population": pandas.Series([1, 1, 1, 1, 1, 1, 1, 1, 1, 1]),
            "value": pandas.Series([0, 1, 1, 0, 1, 0, 1, 1, 0, 1]),
            "date": pandas.Series(
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
            ),
        }
    )
    testing.assert_frame_equal(obs, exp)



