# Only if cnx is none, then create the connection
import mysql.connector
__cnx = None

def get_sql_connection():
    global __cnx
    if __cnx is None:
        __cnx = mysql.connector.connect(user='root', password='Wjdgns7278!', host='127.0.0.1',
                                database='supermarket')   
    return __cnx