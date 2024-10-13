import mysql.connector
import configparser
from mysql.connector import pooling


def read_db_config(filename='db_config.ini', section='mysql'):
    config = configparser.ConfigParser()
    config.read(filename)
    db_config ={}
    if config.has_section(section):
        params = config.items(section)
        for param in params:
            db_config[param[0]] = param[1]
    else:
        raise Exception('Section {0} not found in the {1} file'.format(section, filename))

    return db_config

def connect_to_db():
    try:
        db_config =read_db_config()

        connection = mysql.connector.connect(**db_config)

        if connection.is_connected():
            print('Connected to MySQL database')
            return connection
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None

db_config =read_db_config()
connection_pool = pooling.MySQLConnectionPool(
    pool_name="mypool",
    pool_size=5,
    **db_config
)

def execute_search_query(query, params=None):
    connection = connection_pool.get_connection()
    try:
        cursor = connection.cursor()
        cursor.execute(query, params)
        results = cursor.fetchall()
        return results
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None
    finally:
        cursor.close()
        connection.close()

#
def execute_one_query(query, params=None):
    connection = connection_pool.get_connection()
    try:
        cursor = connection.cursor()
        cursor.execute(query, params)
        connection.commit()
        return cursor.rowcount  #
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None
    finally:
        cursor.close()
        connection.close()

def execute_many_query(query, params=None):
    connection = connection_pool.get_connection()
    try:
        cursor = connection.cursor()
        cursor.executemany(query, params)
        connection.commit()
        return  cursor.rowcount
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None
    finally:
        cursor.close()
        connection.close()








