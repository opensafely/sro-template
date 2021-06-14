import pandas
import pytest
from ..analysis import utilities





@pytest.fixture
def imd_measure_table_from_csv():
    """
    Returns a measure table that could have been read from a CSV file.
    """
    return pandas.DataFrame(
        {
            "imd": pandas.Series([1, 2, 3, 4, 5, 6, 7, 8, 9, 10]),
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

imd_measure_table_from_csv()




