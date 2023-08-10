import os
file_path = os.path.abspath(__file__)
folder_path = os.path.dirname(file_path)
parent_folder_path = os.path.dirname(folder_path)
src_folder_path = os.path.join(parent_folder_path,'src')


from time_range import QueryTime
from set_logging import logger
from create_csv_folder import create_csv_folder
from check_export import check_export
from csv_freight import csv_freight
from csv_surcharge import csv_surcharge

import requests,json

if __name__ == "__main__":

    qt = QueryTime()
    today = qt.current_day()
    folder_name = today.strftime('%Y-%m-%d')

    logging = logger(folder_name)
    csv_folder = create_csv_folder(folder_name)



    time_range = qt.time_range()
    start_utc_time = time_range['start_utc_time']
    end_utc_time = time_range['end_utc_time']
    logging.info(f'\n>>> time range of this week: between {start_utc_time} and {end_utc_time}')

    excluded_accounts = (1,284,317,513,911,2333,4832,1978,2677,3430,3793,3980,5474,5906,6572,6484,6681,6682,6684,6728,6734,6735)



    df_merged = check_export(start_utc_time,end_utc_time,excluded_accounts,csv_folder)
    try:
        if 'F' not in df_merged['checker'].values:

            result = df_merged


            url = "http://52.62.255.169/admin/auth/sysaccount/invoice_v2"

            payload = json.dumps({
                        "eizAccountId": df_merged['account_id'].iloc[:len(df_merged)].to_list(),
                        "from": start_utc_time,
                        "to": end_utc_time
                                })

            headers = {
                        'User-Agent': 'PostmanRuntime/7.31.1',
                        'Content-Type': 'application/json',
                        'Accept': '*/*',
                        'Accept-Encoding': 'gzip, deflate, br',
                        'Connection': 'keep-alive'
                        # 'Authorization': token
                    }
                        
            response = requests.request("GET",url,headers=headers,data=payload)

            json_data = response.json()

            pretty_json = json.dumps(json_data, indent=4)

            print(pretty_json)

            logging.info(f'\n{pretty_json}')


            csv_freight = csv_freight(start_utc_time,end_utc_time,excluded_accounts,csv_folder)

            csv_surcharge = csv_surcharge(start_utc_time,end_utc_time,excluded_accounts,csv_folder)


        elif 'F' in df_merged['checker'].values:
            result = df_merged.loc[df_merged['checker']=='F']
            
        print(result)

        result.to_csv(os.path.join(csv_folder),index=False)
    
    except Exception as e:
        logging.error(f'An error occurred: {e}')
        print(f'An error occurred: {e}')
