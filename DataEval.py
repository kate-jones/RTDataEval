import requests
import datetime
from dateutil.relativedelta import relativedelta


'''
Realtime Data Eval Script uses an NWIS url to obtain DV's for all UTWSC sites for the seven major pcodes.
district_cd=49 can be changed to run for other WSC's.
'''

'''
Initialize variables.
'''

start_time_dt = datetime.datetime.now()  # Current date and time
eval_dates = []  # List of eval date strings for use in url

run_date_str = start_time_dt.strftime('%Y%m%d_%H%m%S')  # String for filename
increment_eval_date = datetime.datetime(2018, 10, 1)

parameters = {'00060': 'q', '72019': 'wl', '00010': 'wt', '00095': 'sc', '00400': 'ph', '00300': 'do', '63680': 'turb'}

'''
Set last retrieval date to today if not the first of the month, otherwise to last month, to avoid retrieval of a partial day.
'''

if start_time_dt.strftime('%d') != '01':
  last_time_dt = start_time_dt
else:
  last_time_dt = start_time_dt - relativedelta(months=1)
print(last_time_dt)

'''
Create list of retrieval dates for first of each month since script was first run.
'''

while last_time_dt > increment_eval_date:
  increment_eval_date_str = increment_eval_date.strftime('%Y-%m-%d')
  eval_dates.append(increment_eval_date_str)
  increment_eval_date = increment_eval_date + relativedelta(months=1)

print('\n\nRetrieving DV information for the following Parameter Codes:\n 00065: Discharge\n 72019: Groundwater Level\n 00010: Water Temperature\n 00095: Specific Conductance\n 00400: pH\n 00300: Dissolved Oxygen\n 63680: Turbidity\nRetrieval takes several minutes....\n\n')

'''
Loop through date list for retrieval of each parameter. Use requests library to query url string.
'''

for pcode in parameters.keys():

  for ind_date in eval_dates:

    url = f'https://waterdata.usgs.gov/nwis/dv?referred_module=qw&district_cd=49&nw_longitude_va=-179&nw_latitude_va=89&se_longitude_va=-1&se_latitude_va=1&coordinate_format=decimal_degrees&index_pmcode_{pcode}=1&group_key=NONE&sitefile_output_format=html_table&column_name=agency_cd&column_name=site_no&column_name=station_nm&range_selection=date_range&begin_date={ind_date}&end_date={ind_date}&format=rdb&date_format=YYYY-MM-DD&rdb_compression=value&list_of_search_criteria=lat_long_bounding_box%2Crealtime_parameter_selection'

    r = requests.get(url)
    content = r.text

    '''
    Write results for all retrieval dates to one file for each parameter.
    '''

    with open(f'dv_{parameters[pcode]}_{run_date_str}.rdb', 'a') as f:
        f.write(content)

  print(f'Retrieval complete for {parameters[pcode]}.\nScript execution time for {parameters[pcode]}: {datetime.datetime.now() - start_time_dt} seconds')

print('\n\nFiles created.\nRetrieval complete for all parameters.')