import requests
import datetime
from dateutil.relativedelta import relativedelta


'''
Realtime Data Eval Script uses an NWIS url to obtain DV's for all UTWSC sites for the seven major pcodes.
district_cd=49 can be changed to run for other WSC's.
Retrieves DV's for the first day of each month, every day for a year. 
On the second day of each month it starts retrievals for a new day. 
After user has been running it daily for at least a year it is always retrieving 12 days.

Instructions: Edit the increment_eval_date variable below to match the day you want the script to start running, then schedule it using cron or Windows Task Scheduler.
If implementing this script for the first time or after a break in usage, the increment_eval_date below must be set.
Do not edit other instances of the increment_eval_date variable.
'''

############### Edit this line only. ###############
increment_eval_date = datetime.datetime(2019, 4, 1)
####################################################

'''
Initialize variables.
'''

start_time_dt = datetime.datetime.now()  # Current date and time
last_time_dt = start_time_dt - relativedelta(days=1)
eval_dates = []  # List of eval date strings for use in url

run_date_str = start_time_dt.strftime('%Y%m%d_%H%m%S')  # String for filename
if start_time_dt < increment_eval_date:
  quit()
one_year_eval_date = last_time_dt - relativedelta(months=11)
if one_year_eval_date > increment_eval_date:
  increment_eval_date = one_year_eval_date

parameters = {'00060': 'q', '72019': 'wl', '00010': 'wt', '00095': 'sc', '00400': 'ph', '00300': 'do', '63680': 'turb'}

'''
Create list of retrieval dates for first of each month since script was first run.
'''

while last_time_dt > increment_eval_date:
  increment_eval_date_str = f"{increment_eval_date.strftime('%Y-%m')}-01"
  eval_dates.append(increment_eval_date_str)
  increment_eval_date = increment_eval_date + relativedelta(months=1)

if start_time_dt.strftime('%d') != '01' and start_time_dt != increment_eval_date:
  start_time_str = f"{start_time_dt.strftime('%Y-%m')}-01"
  eval_dates.append(start_time_str)

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

  print(f'Retrieval complete for {parameters[pcode]}.\nScript execution time for {parameters[pcode]}: {datetime.datetime.now() - start_time_dt}')

print('\n\nFiles created.\nRetrieval complete for all parameters.')