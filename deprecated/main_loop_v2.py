#first file
import mysql.connector as mysql
from tabulate import tabulate
from credentials import return_credentials
from helping_f import helping_functions
from datetime import datetime, timedelta
import time
DEBUG_LEVEL = 0

printd = helping_functions(DEBUG_LEVEL).printd
credentials = return_credentials()
orders={}

#Credentials:
HOST = credentials["HOST"]
DATABASE = credentials["DATABASE"]
USER = credentials["USER"]
PASSWORD = credentials["PASSWORD"]

#connect to the db
db_connection = mysql.connect(host=HOST, database=DATABASE, user=USER, password=PASSWORD)

def fetch_data(db_connection):   
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
    printd(tabulate(rows, headers=cursor.column_names),0)
    
    orders={}
    for i in range(len(rows)):
        order = {"user":rows[i][1], "time_finish":rows[i][2], "food_type":rows[i][3], "food_amount":rows[i][4], "time_ordered":rows[i][5]}
        orders[str(i)] = order

    printd((order["user"], order["time_finish"], order["food_type"], order["food_amount"], order["time_ordered"]),1)
    printd(orders,1)

    for i in range(len(orders)):
        printd(orders[str(i)],1)
        if orders[str(i)]["time_finish"] > now:
            print(orders[str(i)]["user"],"'s food is going to be prepared")
        elif orders[str(i)]["time_finish"] < now:
            print(orders[str(i)]["user"],"'s food has been prepared")
    #orders contain now all orders
    return orders, cursor


now = datetime.now() # time object
print(now.strftime("%d.%m.%Y, %H:%M"))

try:
    while True:
        current_time = datetime.now()
        print(now)
        if ((now + timedelta(seconds=30)).strftime("%d.%m.%Y, %H:%M")) == current_time.strftime("%d.%m.%Y, %H:%M"):
            print("[+]Two minutes passed, prepare to fetch new orders")
            (fetch, cursor) = fetch_data(db_connection)
            now = datetime.now()
        else:
            time.sleep(5)
            print("[+]Sleeping...")
except KeyboardInterrupt:
    pass


# close the cursor
cursor.close()
# close the DB connection
db_connection.close()
