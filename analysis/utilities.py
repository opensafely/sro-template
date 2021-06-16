import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import json
import datetime
from dateutil.relativedelta import relativedelta
import os
from urllib.request import urlopen
from pandas.api.types import is_numeric_dtype


def calculate_imd_group(df, disease_column, rate_column):
    """Converts imd column from ordinal to quantiles and groups by these quintiles.
    
    Args:
        df: measures df with "imd" column.
        disease_column: column name of events column
        rate_column: column name of rate column

    Returns:
        Measures dataframe by IMD quintile
    """
    
    imd_column = pd.to_numeric(df["imd"])
    df["imd"] = pd.qcut(imd_column, q=5,duplicates="drop", labels=['Most deprived', '2', '3', '4', 'Least deprived'])   
    df_rate = df.groupby(by=["date", "imd"])[[rate_column]].mean().reset_index()
    df_population = df.groupby(by=["date", "imd"])[[disease_column, "population"]].sum().reset_index()
    df_merged = df_rate.merge(df_population, on=["date", "imd"], how="inner")
    
    return df_merged[['imd', disease_column, 'population', rate_column, 'date']]

def redact_small_numbers(df, n, numerator, denominator, rate_column):
    """Takes counts df as input and suppresses low numbers.  Sequentially redacts
    low numbers from numerator and denominator until count of redcted values >=n.
    Rates corresponding to redacted values are also redacted.
    
    Args:
        df: measures dataframe
        n: threshold for low number suppression
        numerator: column name for numerator
        denominator: column name for denominator
        rate_column: column name for rate
    
    Returns:
        Input dataframe with low numbers suppressed
    """
    
    def suppress_column(column):    
        suppressed_count = column[column<=n].sum()
        
        #if 0 dont need to suppress anything
        if suppressed_count == 0:
            pass
        
        else:
            column = column.replace([0, 1, 2, 3, 4, 5],np.nan)
            

            while suppressed_count <=n:
                suppressed_count += column.min()
                column.iloc[column.idxmin()] = np.nan   
        return column
    
    
    for column in [numerator, denominator]:
        df[column] = suppress_column(df[column])
    
    df.loc[(df[numerator].isna())| (df[denominator].isna()), rate_column] = np.nan
    
    return df    

def convert_ethnicity(df):
    ethnicity_codes = {1.0: "White", 2.0: "Mixed", 3.0: "Asian", 4.0: "Black", 5.0:"Other", np.nan: "unknown", 0: "unknown"}

    df = df.replace({"ethnicity": ethnicity_codes})
    return df

def calculate_rate(df, numerator, denominator, rate_per=1000):
    num_per_thousand = df[numerator]/(df[denominator]/rate_per)
    df['rate'] = num_per_thousand
    
    return df
        
def drop_irrelevant_practices(df):
    #drop practices that do not use the code
    mean_value_df = df.groupby("practice")["value"].mean().reset_index()

    practices_to_drop = list(
        mean_value_df['practice'][mean_value_df['value'] == 0])

    #drop
    df = df[~df['practice'].isin(practices_to_drop)]

    return df


def plot_measures(df, title, column_to_plot, category=False, y_label='Rate per 1000'):

    if category:
        for unique_category in df[category].unique():

            df_subset = df[df[category] == unique_category]

            plt.plot(df_subset['date'], df_subset[column_to_plot], marker='o')
    else:
        plt.plot(df['date'], df[column_to_plot], marker='o')

    plt.ylabel(y_label)
    plt.xlabel('Date')
    plt.xticks(rotation='vertical')
    plt.title(title)

    if category:
        plt.legend(df[category].unique(), bbox_to_anchor=(
            1.04, 1), loc="upper left")

    else:
        pass


    plt.show()
    plt.clf()


def get_child_codes(df):

    event_code_column = 'event_code'
    event_column = 'event'

    counts = df.groupby(event_code_column)[event_column].sum()
    code_dict = dict(counts)

    return code_dict

def create_child_table(df, code_df, code_column, term_column, nrows=5):
    #pass in df from data_dict
    #code df contains first digits and descriptions

    #get codes counts
    code_dict = get_child_codes(df)

    #make df of events for each subcode
    df = pd.DataFrame.from_dict(
        code_dict, orient="index", columns=["Events"])
    df[code_column] = df.index

    #convert snomed
    if is_numeric_dtype(df[code_column]):
        
      
        df = df.astype({code_column: 'int64'})
        df.reset_index(drop=True, inplace=True)

    #convert events to events/thousand
    df['Events (thousands)'] = df['Events'].apply(lambda x: x/1000)
    df.drop(columns=['Events'])

    #order by events
    df.sort_values(by='Events (thousands)', inplace=True)
    df = df.iloc[:, [1, 0, 2]]

    #get description for each code

    def get_description(row):
        code = row[code_column]

        description = code_df[code_df[code_column]
                              == code][term_column].values[0]

        return description

    df['Description'] = df.apply(
        lambda row: get_description(row), axis=1)

    #return top n rows
    return df.iloc[:nrows, :]


def get_number_practices(df, end_date):
    
    num_practices_total = len(np.unique(df['practice']))

    end_date = datetime.datetime.strptime(
        end_date, '%Y-%m-%d')


    year_before = end_date - relativedelta(years=1)
    months_3_before = end_date - relativedelta(months=3)

    df_subset_year = df[df['date'] > year_before]
    num_practices_year = len(np.unique(df_subset_year['practice']))

    df_subset_months_3 = df[df['date'] > months_3_before]
    num_practices_months_3 = len(np.unique(df_subset_months_3['practice']))

    numbers_dict = {"total": num_practices_total, "year": num_practices_year, "3_months": num_practices_months_3}
    return numbers_dict

def calculate_statistics_practices(df, practice_df, end_date):

    
    num_practices = len(np.unique(practice_df['practice']))


    # calculate number of unique practices and caluclate as % of total
    practices_included_total = get_number_practices(df, end_date)['total']
    practices_included_year = get_number_practices(df, end_date)['year']
    practices_included_months_3 = get_number_practices(df, end_date)['3_months']


    practices_included_percent_total = float(
        f'{((practices_included_total/num_practices)*100):.2f}')
    
    practices_included_percent_year = float(
        f'{((practices_included_year/num_practices)*100):.2f}')

    practices_included_percent_months_3 = float(
        f'{((practices_included_months_3/num_practices)*100):.2f}')


    return {"total": {"number": practices_included_total, "percent": practices_included_percent_total}, "year": {"number": practices_included_year, "percent": practices_included_percent_year}, "months_3": {"number": practices_included_months_3, "percent": practices_included_percent_months_3}}
    

