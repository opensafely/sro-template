from utilities import *
from pathlib import Path
import pandas as pd
import os
from cohortextractor import Measure
from study_definition import measures
from config import demographics, codelist_path
from ebmdatalab import charts

BASE_DIR = Path(__file__).parents[1]
OUTPUT_DIR = BASE_DIR / "output"

measures_dict = {}

for m in measures:
    measures_dict[m.id] = m

for key, value in measures_dict.items():
    
    df = pd.read_csv(os.path.join(OUTPUT_DIR, f'measure_{value.id}.csv'), parse_dates=['date']).sort_values(by='date')
    df = drop_missing_demographics(df, value.group_by[0])
    
    # get total population rate
    if value.id=='practice_rate':
        
        df = drop_irrelevant_practices(df, 'practice')
        df.to_csv(os.path.join(OUTPUT_DIR, f'rate_table_{value.group_by[0]}.csv'), index=False)

        charts.deciles_chart(
        df,
        period_column='date',
        column='event',
        title='Decile Chart',
        ylabel='Proportion',
        show_outer_percentiles=False,
        show_legend=True,
        ).savefig('output/decile_chart.png', bbox_inches='tight')  
        
    elif value.id=='event_code_rate':
        codelist = pd.read_csv(codelist_path)
        child_code_table = create_child_table(df=df, code_df=codelist, code_column='code', term_column='term')
        child_code_table.to_csv('output/child_code_table.csv', index=False)

    elif value.id=='population_rate':
        plot_measures(df, filename=f'plot_{value.group_by[0]}.png', title=f'Breakdown by {value.group_by[0]}', column_to_plot='value', category=False, y_label='Proportion')
        

    else:
        plot_measures(df, filename=f'plot_{value.group_by[0]}.png', title=f'Breakdown by {value.group_by[0]}', column_to_plot='value', category=value.group_by[0], y_label='Proportion')
        