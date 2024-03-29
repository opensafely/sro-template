import pandas as pd
from pathlib import Path
from study_definition import measures
from utilities import redact_small_numbers

BASE_DIR = Path(__file__).parents[1]
OUTPUT_DIR = BASE_DIR / "output/joined"

measures_dict = {}

for m in measures:
    measures_dict[m.id] = m

if __name__ == '__main__':
    for key, value in measures_dict.items():
        
        df = pd.read_csv(OUTPUT_DIR / f'measure_{value.id}.csv', parse_dates=['date']).sort_values(by='date')
        df = redact_small_numbers(df, 5, value.numerator, value.denominator, 'value', 'date')
        df.to_csv(OUTPUT_DIR / f'measure_{value.id}.csv')