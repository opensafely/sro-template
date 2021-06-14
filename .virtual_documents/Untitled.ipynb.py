import pandas
import pytest
from analysis import utilities


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


def test_calculate_imd_group(imd_measure_table_from_csv):

    utilities.calculate_imd_group(imd_measure_table_from_csv, 'event', 'rate')
    


test = pandas.DataFrame(
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



test


import pandas as pd
def calculate_imd_group(df, disease_column, rate_column):
    
    imd_column = pd.to_numeric(df["imd"])
    df["imd"] = pd.qcut(imd_column, q=5,duplicates="drop", labels=['Most deprived', '2', '3', '4', 'Least deprived'])      
    df_rate = df.groupby(by=["date", "imd"])[[rate_column]].mean().reset_index()
    df_population = df.groupby(by=["date", "imd"])[[disease_column, "population"]].sum().reset_index()
    df_merged = df_rate.merge(df_population, on=["date", "imd"], how="inner")
    
    return df_merged[['imd', disease_column, 'population', rate_column, 'date']]


obs = calculate_imd_group(test, 'event', 'value')


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


exp


pd.testing.assert_frame_equal(obs, exp)



