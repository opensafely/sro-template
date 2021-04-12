import pandas as pd
import os


ethnicity_imd_df = pd.read_csv('output/input_ethnicity.csv')


for file in os.listdir('output'):
    if file.startswith('input'):
        #exclude ethnicity
        if file.split('_')[1] != 'ethnicity':
            file_path = os.path.join('output', file)
            df = pd.read_csv(file_path)
            merged_df = df.merge(ethnicity_imd_df, how='left', on='patient_id')
            
            merged_df.to_csv(file_path)