#first file
import mysql.connector as mysql
import time

from tabulate import tabulate
from credentials import return_credentials
from helping_f import helping_functions
from datetime import datetime, timedelta
credentials = return_credentials()

from fetch_data import fetch_data
DEBUG_LEVEL = 0

now = datetime.now() # time object
printd = helping_functions(DEBUG_LEVEL).printd
fetch_data = fetch_data(credentials)

#Credentials:
HOST = credentials["HOST"]
DATABASE = credentials["DATABASE"]
USER = credentials["USER"]
PASSWORD = credentials["PASSWORD"]

#connect to the db
db_connection = mysql.connect(host=HOST, database=DATABASE, user=USER, password=PASSWORD)

#get server information
print(db_connection.get_server_info())

#get the db cursor
cursor = db_connection.cursor()

#get the database information
cursor.execute("select database();")
database_name = cursor.fetchone()
print("[+] You are connected to the database:", database_name)

#fetch the database
cursor.execute("select * from orders")
#get all selected rows
rows = cursor.fetchall()
#print all orders(rows) in a table with tabulate
printd(tabulate(rows, headers=cursor.column_names),1)

orders={}


now = datetime.now()
print("[+]",now.strftime("%d.%m.%Y, %H:%M"))

try:
    while True:
        current_time = datetime.now()
        if ((now + timedelta(minutes=1)).strftime("%d.%m.%Y, %H:%M")) == current_time.strftime("%d.%m.%Y, %H:%M"):
            print("[+]Two minutes passed, prepare to fetch new orders")
            fetch_data()
            #print(fetched_data)
            #orders, orders_old_format = fetched_data
            #print("In the current fetch: ",orders)
            #print(tabulate(orders_old_format, headers=cursor.column_names))
            now = datetime.now()
        else:
            print("[+]Sleeping...")
            time.sleep(15)
            
except KeyboardInterrupt:
    pass
# close the cursor
cursor.close()
# close the DB connection
db_connection.close()