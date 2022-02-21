from redact_measures import measures_dict
from utilities import OUTPUT_DIR, create_top_5_code_table
from config import codelist_path

codelist = pd.read_csv(codelist_path)

for key, value in measures_dict.items():
    if value.id == 'event_code_rate':
        df = pd.read_csv(os.path.join(OUTPUT_DIR, 'measure_event_code_rate.csv'), parse_dates=['date']).sort_values(by='date')
        top_5_code_table = create_top_5_code_table(df=df, code_df=codelist, code_column='code', term_column='term')
        top_5_code_table.to_csv(os.path.join(OUTPUT_DIR, 'top_5_code_table.csv'), index=False)