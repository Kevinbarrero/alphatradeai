import psycopg2
import pandas as pd


def get_db_data(coin):
    global connection, cursor
    try:
        connection = psycopg2.connect(user="tradingmanager",
                                      password="tradingmanager",
                                      host="localhost",
                                      port="5432",
                                      database="tradingmanager")
        cursor = connection.cursor()
        postgreSQL_select_Query = "select * from " + coin

        cursor.execute(postgreSQL_select_Query)
        model_records = cursor.fetchall()
        train_data = pd.DataFrame(model_records,
                                  columns=['open_time', 'open', 'high', 'low', 'close', 'volume', 'close_time',
                                           'n_trades'])
        train_data = train_data.sort_values(by='open_time').reset_index(drop=True)

        return train_data
    except Exception:
        return None
    finally:
        if connection:
            cursor.close()
            connection.close()
