import requests
import datetime


start_time = datetime.datetime.now()
run_date = start_time.strftime('%Y%m%d_%H%m%S')
run_month = start_time.strftime('%Y-%m')
eval_date = f'{run_month}-01'

parameters = {'00060': 'q', '72019': 'wl', '00010': 'wt', '00095': 'sc', '00400': 'ph', '00300': 'do', '63680': 'turb'}

for pcode in parameters.keys():

  url = f'https://waterdata.usgs.gov/nwis/dv?referred_module=qw&district_cd=49&nw_longitude_va=-179&nw_latitude_va=89&se_longitude_va=-1&se_latitude_va=1&coordinate_format=decimal_degrees&index_pmcode_{pcode}=1&group_key=NONE&sitefile_output_format=html_table&column_name=agency_cd&column_name=site_no&column_name=station_nm&range_selection=date_range&begin_date={eval_date}&end_date={eval_date}&format=rdb&date_format=YYYY-MM-DD&rdb_compression=value&list_of_search_criteria=lat_long_bounding_box%2Crealtime_parameter_selection'

  r = requests.get(url)
  content = r.text

  with open(f'dv_{parameters[pcode]}_{run_date}.rdb', 'a') as f:
      f.write(content)

  print(f'Script execution time for {parameters[pcode]}: {datetime.datetime.now() - start_time} seconds')