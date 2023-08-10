import os

from db_connect import ExecuteQuery
from time_range import QueryTime
from set_logging import create_logger


qt = QueryTime()
today = qt.current_day()
date = today.strftime("%Y%m%d")

folder_name = today.strftime('%Y-%m-%d')

logging = create_logger(folder_name)


def csv_freight(start_utc_time,end_utc_time,excluded_accounts,csv_folder):
    db_config_name = 'db.ini' 

    db_test = 'eiz_test'
    db_sf1 = 'eiz-resell'
    db_sf2 = 'eiz_resell'
    # db_supplier = 'eiz_supplier'

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


            params_consign_id = {
                                'start_time': start_utc_time,
                                'end_time': end_utc_time,
                                'account_id': account_id
                                }
            query_consignment_id = 'consignment_id.sql'
            eq_consignment_id = ExecuteQuery(db_test,params_consign_id,db_config_name,query_consignment_id)
            df_consignment_id = eq_consignment_id.execute_query()

            consignment_id = tuple(df_consignment_id['consignment_id'])




            params_statement_num = {
                                    'consignment_id': consignment_id
                                    }
            query_statement_num_sf1 = 'statement_num_sf1.sql'
            eq_statement_num_sf1 = ExecuteQuery(db_sf1,params_statement_num,db_config_name,query_statement_num_sf1)
            df_statement_num_sf1 = eq_statement_num_sf1.execute_query()

            if df_statement_num_sf1.empty == False:

                statement_num = df_statement_num_sf1['statement_num'].values.tolist()[0]

            else:

                query_statement_num_sf2 = 'statement_num_sf2.sql'
                eq_statement_num_sf2 = ExecuteQuery(db_sf2,params_statement_num,db_config_name,query_statement_num_sf2)
                df_statement_num_sf2 = eq_statement_num_sf2.execute_query()

                statement_num = df_statement_num_sf2['statement_num'].values.tolist()[0]



            params_invoice_id = {
                                    'statement_num': str(statement_num)
                                }
            query_invoice_id = 'invoice_id.sql'
            eq_invoice_id = ExecuteQuery(db_test,params_invoice_id,db_config_name,query_invoice_id)
            df_invoice_id = eq_invoice_id.execute_query()

            invoice_id = df_invoice_id['id'].values.tolist()[0]
                # 整合invoice_number字段
            if len(str(invoice_id)) == 6:
                invoice_number = 'L00'+str(invoice_id)
            elif len(str(invoice_id)) == 7:
                invoice_number = 'L0'+str(invoice_id)
            else:
                invoice_number = 'L'+str(invoice_id)




            params_csv_freight = {
                                    'invoice_number': invoice_number,
                                    'account_id': account_id,
                                    'start_time': start_utc_time,
                                    'end_time': end_utc_time
                                }
            query_csv_freight = 'csv_freight.sql'
            eq_csv_freight = ExecuteQuery(db_test,params_csv_freight,db_config_name,query_csv_freight)
            df_csv_freight = eq_csv_freight.execute_query()

            df_csv_freight.to_csv(os.path.join(csv_folder,f'{company_name}({account_id})_{date}.csv'),index=False)

            print(f'{account_id},{statement_num},{invoice_id},{len(df_csv_freight)}')
            logging.info(f'{account_id},{statement_num},{invoice_id},{len(df_csv_freight)}')
            logging.info(f'\n{df_csv_freight}')


        except Exception as e:
            logging.error(f'An error occurred: {e}')
            print(f'An error occurred: {e}')


if __name__ == "__main__":

    from create_csv_folder import create_csv_folder

    qt = QueryTime()
    today = qt.current_day()
    folder_name = today.strftime('%Y-%m-%d')

    logging = create_logger(folder_name)
    csv_folder = create_csv_folder(folder_name)

    time_range = qt.time_range()
    start_utc_time = time_range['start_utc_time']
    end_utc_time = time_range['end_utc_time']
    logging.info(f'\n>>> time range of this week: between {start_utc_time} and {end_utc_time}')

    excluded_accounts = (1,284,317,513,911,2333,4832,1978,2677,3430,3793,3980,5474,5906,6572,6484,6681,6682,6684,6728,6734,6735)

    csv_freight(start_utc_time,end_utc_time,excluded_accounts,csv_folder)