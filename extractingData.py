import mysql.connector
from mysql.connector import Error

try:
    connection = mysql.connector.connect(host="localhost",
                                         user="root",
                                         passwd="",
                                         database="schema1")

    sql_select_Query = "SELECT data " \
                       "FROM twitter_table " \
                       "Where twitter_table.created_at >= ‘2020-03-16 00:00’ and twitter_table.created_at <= ‘2020-03-16 15:00’"
    #TIME
    cursor = connection.cursor()
    cursor.execute(sql_select_Query)
    records = cursor.fetchall()
    print("Total number of rows in Laptop is: ", cursor.rowcount)

    print("\nPrinting each laptop record")
    for row in records:
        print("Id = ", row[0], )
        print("created_at = ", row[1])
        print("datetime_parsed  = ", row[2], "\n")

except Error as e:
    print("Error reading data from MySQL table", e)
finally:
    if (connection.is_connected()):
        connection.close()
        cursor.close()
        print("MySQL connection is closed")