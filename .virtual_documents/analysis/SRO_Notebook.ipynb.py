import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()
from IPython.display import HTML
from IPython.display import Markdown as md
from IPython.core.display import HTML as Center
from utilities import *
from config import marker, start_date, end_date, demographics, codelist_path
from ebmdatalab import charts

get_ipython().run_line_magic("matplotlib", " inline")


class Measure:
  def __init__(self, id, numerator, denominator, group_by, small_number_suppression):
    self.id = id
    self.numerator = numerator
    self.denominator = denominator
    self.group_by = group_by
    self.small_number_suppression = small_number_suppression
    

# Create default measures
measures = [

    Measure(
        id="event_code_rate",
        numerator="event",
        denominator="population",
        group_by=["event_code"],
        small_number_suppression=True
    ),

    Measure(
        id="practice_rate",
        numerator="event",
        denominator="population",
        group_by=["practice"],
        small_number_suppression=False
    ),



]


#Add demographics measures

for d in demographics:

    if d == 'imd':
        apply_suppression = False
    
    else:
        apply_suppression = True
    
    m = Measure(
        id=f'{d}_rate',
        numerator="event",
        denominator="population",
        group_by=[d],
        small_number_suppression=apply_suppression
    )
    
    measures.append(m)


default_measures = ['event_code', 'practice']
measures_ids = default_measures+ demographics
measures_dict = {}

for m in measures:
    measures_dict[m.id] = m







display(
md("# Service Restoration Observatory"),
md(f"## Changes in {marker} between {start_date} and {end_date}"),
md(f"Below are various time-series graphs showing changes in {marker} code use."),
)



display(
md("### Methods"),
md(f"Using OpenSAFELY-TPP, covering 40% of England's population, we have assessed coding activity related to {marker} between {start_date} and {end_date}. The codelist used can be found here at [OpenSAFELY Codelists](https://codelists.opensafely.org/).  For each month within the study period, we have calculated the rate at which the code was recorded per 1000 registered patients."),
md(f"All analytical code and output is available for inspection at the [OpenSAFELY GitHub repository](https://github.com/opensafely")
)



default_measures = ['event_code', 'practice']
measures = default_measures+ demographics

data_dict = {}

for key, value in measures_dict.items():
    
    df = pd.read_csv(f'../output/measure_{value.id}.csv')
    

    to_datetime_sort(df)
    

    if key == "imd":
        df = calculate_imd_group(df, 'event', 'rate_standardised')
        
    elif key == "ethnicity":
        df = convert_ethnicity(df)
        
    df = calculate_rate(df, numerator=value.numerator, denominator=value.denominator, rate_per=1000)
    
    if key == "imd":
        df = redact_small_numbers(df, 5, value.numerator, value.denominator, 'rate')
    
    
    # get total population rate
    if value.id=='practice_rate':
        
        df = drop_irrelevant_practices(df)
        
        df_total = df.groupby(by='date')[[value.numerator, value.denominator]].sum().reset_index()
        df_total = calculate_rate(df_total, numerator=value.numerator, denominator=value.denominator, rate_per=1000)
        data_dict['total'] = df_total
    
    data_dict[value.id] = df
    
codelist = pd.read_csv(f'../{codelist_path}')



display(
md(f"## Total {marker} Number")
)



plot_measures(data_dict['total'], title=f"Total {marker} across whole population", column_to_plot='rate', category=False, y_label='Rate per 1000')



display(
md("### Sub totals by sub codes"),
md("Events for the top 5 subcodes across the study period"))
child_table = create_child_table(df=data_dict['event_code_rate'], code_df=codelist, code_column='code', term_column='term')
child_table
    


display(
md("## Total Number by GP Practice")
)




practice_files = []
for file in os.listdir('../output'):
    if file.startswith('input_practice_count'):
        df = pd.read_csv(os.path.join('../output',file))
        practice_files.append(df)

practice_df = pd.concat(practice_files)
practices_dict =calculate_statistics_practices(data_dict['practice_rate'], practice_df,end_date)
print(f'Practices included entire period: {practices_dict["total"]["number"]} ({practices_dict["total"]["percent"]}get_ipython().run_line_magic(")')", "")
print(f'Practices included within last year: {practices_dict["year"]["number"]} ({practices_dict["year"]["percent"]}get_ipython().run_line_magic(")')", "")
print(f'Practices included within last 3 months: {practices_dict["months_3"]["number"]} ({practices_dict["months_3"]["percent"]}get_ipython().run_line_magic(")')", "")

charts.deciles_chart(
        data_dict['practice_rate'],
        period_column='date',
        column='event',
        title='Decile Chart',
        ylabel='rate per 1000',
        show_outer_percentiles=False,
        show_legend=True,
)



i=0



    display(
    md(f"## Breakdown by {demographics[i]}")
    )
   
    


    plot_measures(data_dict[f'{demographics[i]}_rate'], title=f'Breakdown by {demographics[i]}', column_to_plot='rate', category=demographics[i], y_label='Rate per 1000')
    i+=1
    


    display(
    md(f"## Breakdown by {demographics[i]}")
    )
   
    


    plot_measures(data_dict[f'{demographics[i]}_rate'], title=f'Breakdown by {demographics[i]}', column_to_plot='rate', category=demographics[i], y_label='Rate per 1000')
    i+=1
    


    display(
    md(f"## Breakdown by {demographics[i]}")
    )
   
    


    plot_measures(data_dict[f'{demographics[i]}_rate'], title=f'Breakdown by {demographics[i]}', column_to_plot='rate', category=demographics[i], y_label='Rate per 1000')
    i+=1
    


    display(
    md(f"## Breakdown by {demographics[i]}")
    )
   
    


    plot_measures(data_dict[f'{demographics[i]}_rate'], title=f'Breakdown by {demographics[i]}', column_to_plot='rate', category=demographics[i], y_label='Rate per 1000')
    i+=1
    


    display(
    md(f"## Breakdown by {demographics[i]}")
    )
   
    


    plot_measures(data_dict[f'{demographics[i]}_rate'], title=f'Breakdown by {demographics[i]}', column_to_plot='rate', category=demographics[i], y_label='Rate per 1000')
    i+=1
    


    display(
    md(f"## Breakdown by {demographics[i]}")
    )
   
    


    plot_measures(data_dict[f'{demographics[i]}_rate'], title=f'Breakdown by {demographics[i]}', column_to_plot='rate', category=demographics[i], y_label='Rate per 1000')
    i+=1
    


    display(
    md(f"## Breakdown by {demographics[i]}")
    )
   
    


    plot_measures(data_dict[f'{demographics[i]}_rate'], title=f'Breakdown by {demographics[i]}', column_to_plot='rate', category=demographics[i], y_label='Rate per 1000')
    i+=1
    
