import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
from pathlib import Path

BASE_DIR = Path(__file__).parents[1]
OUTPUT_DIR = BASE_DIR / "output"
ANALYSIS_DIR = BASE_DIR / "analysis"


def match_input_files(file: str) -> bool:
    """Checks if file name has format outputted by cohort extractor"""
    pattern = r"^input_20\d\d-(0[1-9]|1[012])-(0[1-9]|[12][0-9]|3[01])\.feather"
    return True if re.match(pattern, file) else False


def join_ethnicity(directory: str) -> None:
    """Finds 'input_ethnicity.feather' in directory and combines with each input file."""

    dirpath = Path(directory)
    filelist = dirpath.iterdir()

    # get ethnicity input file
    ethnicity_df = pd.read_feather(dirpath / "input_ethnicity.feather")
    ethnicity_dict = dict(zip(ethnicity_df["patient_id"], ethnicity_df["ethnicity"]))

    for file in filelist:
        if match_input_files(file.name):
            df = pd.read_feather(dirpath / file.name)
            df["ethnicity"] = df["patient_id"].map(ethnicity_dict)
            df.to_feather(dirpath / file.name)


def redact_small_numbers(df, n, numerator, denominator, rate_column, date_column):
    """
    Takes counts df as input and suppresses low numbers.  Sequentially redacts
    low numbers from numerator and denominator until count of redcted values >=n.
    Rates corresponding to redacted values are also redacted.
    df: input df
    n: threshold for low number suppression
    numerator: numerator column to be redacted
    denominator: denominator column to be redacted
    """

    def suppress_column(column):
        suppressed_count = column[column <= n].sum()

        # if 0 dont need to suppress anything
        if suppressed_count == 0:
            pass

        else:
            column[column <= n] = np.nan

            while suppressed_count <= n:
                suppressed_count += column.min()

                column[column.idxmin()] = np.nan
        return column

    df_list = []

    dates = df[date_column].unique()

    for d in dates:
        df_subset = df.loc[df[date_column] == d, :]

        for column in [numerator, denominator]:
            df_subset[column] = suppress_column(df_subset[column])

        df_subset.loc[
            (df_subset[numerator].isna()) | (df_subset[denominator].isna()), rate_column
        ] = np.nan
        df_list.append(df_subset)

    return pd.concat(df_list, axis=0)


def convert_binary(df, binary_column, positive, negative):
    """Converts a column with binary variable codes as 0 and 1 to understandable strings.

    Args:
        df: dataframe with binary column
        binary_column: column name of binary variable
        positive: string to encode 1 as
        negative: string to encode 0 as

    Returns:
        Input dataframe with converted binary column
    """
    replace_dict = {0: negative, 1: positive}
    df[binary_column] = df[binary_column].replace(replace_dict)
    return df


def drop_missing_demographics(df, demographic):
    """Drops any rows with missing values for a given demographic variable.

    Args:
        df: measures dataframe
        demographic: column name of demographic variable

    Returns:
        Dataframe with no rows missing demographic variable.
    """
    return df.loc[df[demographic].notnull(), :]


def drop_irrelevant_practices(df, practice_col):
    """Drops irrelevant practices from the given measure table.
    An irrelevant practice has zero events during the study period.
    Args:
        df: A measure table.
        practice_col: column name of practice column
    Returns:
        A copy of the given measure table with irrelevant practices dropped.
    """
    is_relevant = df.groupby(practice_col).value.any()
    return df[df[practice_col].isin(is_relevant[is_relevant == True].index)]


def create_top_5_code_table(df, code_df, code_column, term_column, nrows=5):

    """
    Args:
        df: A measure table.
        code_df: A codelist table.
        code_column: The name of the code column in the codelist table.
        term_column: The name of the term column in the codelist table.
        measure: The measure ID.
        nrows: The number of rows to display.
    Returns:
        A table of the top `nrows` codes.
    """
    event_counts = (
        df.groupby("event_code")["event"]
        .sum()  # We can't use .count() because the measure column contains zeros.
        .rename_axis(code_column)
        .rename("Events")
        .reset_index()
        .sort_values("Events", ascending=False)
    )

    event_counts["Events (thousands)"] = event_counts["Events"] / 1000

    # Gets the human-friendly description of the code for the given row
    # e.g. "Systolic blood pressure".
    code_df = code_df.set_index(code_column).rename(
        columns={term_column: "Description"}
    )
    event_counts = event_counts.set_index(code_column).join(code_df).reset_index()

    # Cast the code to an integer.
    event_counts[code_column] = event_counts[code_column].astype(int)

    # return top n rows

    return event_counts.iloc[:nrows, :]


def get_number_practices(df):
    """Gets the number of practices in the given measure table.
    Args:
        df: A measure table.
    """
    return len(df.practice.unique())


def get_percentage_practices(measure_table):
    """Gets the percentage of practices in the given measure table.
    Args:
        measure_table: A measure table.
    """

    # Read in all input practice count files and get num unique
    practice_df_list = []
    for file in os.listdir(OUTPUT_DIR):
        if file.startswith("input_practice_count"):
            df = pd.read_feather(os.path.join(OUTPUT_DIR, file))
            practice_df_list.append(df)

    total_practices_df = pd.concat(practice_df_list, axis=0)
    num_practices_total = get_number_practices(total_practices_df)

    # Get number of practices in measure
    num_practices_in_study = get_number_practices(measure_table)

    return np.round((num_practices_in_study / num_practices_total) * 100, 2)


def plot_measures(
    df, filename, title, column_to_plot, category=False, y_label="Rate per 1000"
):
    """Produce time series plot from measures table.  One line is plotted for each sub
    category within the category column.

    Args:
        df: A measure table
        title: Plot title string
        column_to_plot: Name of column to plot
        category: Name of column indicating different categories
        y_label: String indicating y axis text
    """
    plt.figure(figsize=(15, 8))
    if category:
        for unique_category in df[category].unique():

            df_subset = df[df[category] == unique_category]

            plt.plot(df_subset["date"], df_subset[column_to_plot], marker="o")
    else:
        plt.plot(df["date"], df[column_to_plot], marker="o")

    plt.ylabel(y_label)
    plt.xlabel("Date")
    plt.xticks(rotation="vertical")
    plt.title(title)

    if category:
        plt.legend(df[category].unique(), bbox_to_anchor=(1.04, 1), loc="upper left")

    else:
        pass

    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / filename)
    plt.clf()
