import os

from db_connect import ExecuteQuery
from time_range import QueryTime
from set_logging import logger


qt = QueryTime()
today = qt.current_day()
date = today.strftime("%Y%m%d")

folder_name = today.strftime('%Y-%m-%d')

logging = logger(folder_name)


def csv_surcharge(start_utc_time,end_utc_time,excluded_accounts,csv_folder):

    db_config_name = 'db.ini' 

    db_test = 'eiz_test'
    # db_sf1 = 'eiz-resell'
    # db_sf2 = 'eiz_resell'
    db_supplier = 'eiz_supplier'

    params_account_id = {
                            'start_time': start_utc_time,
                            'end_time': end_utc_time,
                            'excluded_accounts': excluded_accounts
                        }
    query_account_id = 'account_id.sql'
    eq_account_id = ExecuteQuery(db_test,params_account_id,db_config_name,query_account_id)
    df_account_id = eq_account_id.execute_query()

    list_account_id = df_account_id.to_dict(orient='records')

    for items in list_account_id:

        account_id = items['account_id']
        company_name = items['company_name']

        try: 
            params_surcharge_summary = {
                                            'start_time': start_utc_time,
                                            'end_time': end_utc_time
                                    }
            query_surcharge_summary = 'surcharge_summary.sql'
            eq_surcharge_summary = ExecuteQuery(db_supplier,params_surcharge_summary,db_config_name,query_surcharge_summary)
            df_surcharge_summary = eq_surcharge_summary.execute_query()


            tracking_list = df_surcharge_summary['tracking'].iloc[:len(df_surcharge_summary)].to_list()
            tracking =  "','".join(map(str,tracking_list))




            params_match_surcharge = {
                                        'tracking': "'" + tracking + "'",
                                        'account_id': account_id
                                    }
            query_match_surcharge = 'match_surcharge.sql'
            eq_match_surcharge = ExecuteQuery(db_test,params_match_surcharge,db_config_name,query_match_surcharge)
            df_match_surcharge = eq_match_surcharge.execute_query()

            label_list = list(df_match_surcharge['labels'].values)



            for label in label_list:
                if label in tracking_list:
                    
                    index = int(tracking_list.index(label))

                    invoiceNum = df_surcharge_summary.iloc[index]['invoice_number']
                    # serviceProvider = df_surcharge_summary.iloc[index]['serviceProvider']
                    charge = df_surcharge_summary.iloc[index]['charge']
                    surchargeStatusName = df_surcharge_summary.iloc[index]['status_name']
                    surchargeStatusCode = df_surcharge_summary.iloc[index]['status_code']




                    params_csv_surcharge = {
                                                'invoiceNum':invoiceNum,
                                                'charge':charge,
                                                'surchargeStatusCode':surchargeStatusCode,
                                                'surchargeStatusName':surchargeStatusName,
                                                'label':label,
                                                'account_id':account_id
                                            }
                    query_csv_surcharge = 'csv_surcharge.sql'
                    eq_csv_surcharge = ExecuteQuery(db_test,params_csv_surcharge,db_config_name,query_csv_surcharge)
                    df_csv_surcharge = eq_csv_surcharge.execute_query()

                    df_csv_surcharge.to_csv(os.path.join(csv_folder,f'{company_name}({account_id})_{date}.csv'),mode='a',index=False,header=False)


                    print(f'{account_id},{invoiceNum},{label},{charge}')
                    logging.info(f'{account_id},{invoiceNum},{label},{charge}')
                    logging.info(f'\n{df_csv_surcharge}')
        except Exception as e:
            logging.error(f'An error occurred: {e}')
            print(f'An error occurred: {e}')