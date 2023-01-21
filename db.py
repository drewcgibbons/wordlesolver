# importing the module
import mysql.connector
import pandas as pd

def run_query(sql):

    print(sql)

    # opening a database connection
    cnx = mysql.connector.connect(user='root', password='root',
                              host='127.0.0.1')

    # define a cursor object
    cursor = cnx.cursor()

    data = None

    for result in cursor.execute(sql, multi=True):
        if result.with_rows:
            data = result.fetchall()

    df = pd.DataFrame(data, columns=['Word', 'Frequency'])

    # close object
    cursor.close()

    # close connection
    cnx.close()

    return df