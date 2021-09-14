#first file
import mysql.connector as mysql
import json
import time

from tabulate import tabulate
from credentials import return_credentials
from helping_f import helping_functions
from datetime import datetime, timedelta
DEBUG_LEVEL = 0

now = datetime.now() # time object
printd = helping_functions(DEBUG_LEVEL).printd
credentials = return_credentials()

try:
    f = open("data_recipe.json")
    recipe_data = json.load(f)
except FileNotFoundError as e:
    print("Fatal Error - Recipes not loaded...")
    print("abort")
    print(e)


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

def fetch_data(): 
    db_connection = mysql.connect(host=HOST, database=DATABASE, user=USER, password=PASSWORD)
    print(db_connection.get_server_info())

    cursor = db_connection.cursor()  
    #fetch the database
    cursor.execute("select * from orders")
    #get all selected rows
    rows = cursor.fetchall()
    #print all orders(rows) in a table with tabulate
    #printd(tabulate(rows, headers=cursor.column_names),0)
    #print(rows)
    orders={}
    orders_for_tabulate = []
    for i in range(len(rows)):
        order = {"user":rows[i][1], "time_finish":rows[i][2], "food_type":rows[i][3], "food_amount":rows[i][4], "time_ordered":rows[i][5]}
        if order["time_finish"] > datetime.now():
            #print(order["food_type"], " added to cook")
            orders[str(len(orders))] = order #if it is the first element added(0 elements present) it HAS to be the zeroth element for processing
            orders_for_tabulate.append(rows[i])
        else:
            pass

    printd((order["user"], order["time_finish"], order["food_type"], order["food_amount"], order["time_ordered"]),1)
    printd(orders,1)
    
    for i in range(len(orders)):
        printd(orders[str(i)],1)
        if orders[str(i)]["time_finish"] > now:
            #print(orders[str(i)]["user"],"'s food is going to be prepared")
            pass
        elif orders[str(i)]["time_finish"] < now:
            #print(orders[str(i)]["user"],"'s food has been prepared")
            pass
    #orders contain now all orders
    #print("CURRENT ORDERS:")
    #print("------------------------------------------------")
    #print(tabulate(orders_for_tabulate, cursor.column_names))

    cursor.close()
    db_connection.close()
    return orders, orders_for_tabulate


now = datetime.now()
print("[+]",now.strftime("%d.%m.%Y, %H:%M"))

try:
    while True:
        current_time = datetime.now()
        if ((now + timedelta(minutes=1)).strftime("%d.%m.%Y, %H:%M")) == current_time.strftime("%d.%m.%Y, %H:%M"):
            print("[+]Two minutes passed, prepare to fetch new orders")
            orders, orders_old_format = fetch_data()
            print(tabulate(orders_old_format, headers=cursor.column_names))
            
            for order in orders_old_format:
                current_order = order
                
                for recipe in recipe_data["recipe"]:  
                    if current_order[3] == recipe["compound"]:
                        # OK, now we have the recipe for the coresponding order, which are ordered by time to be executed.
                        print("We have to cook: ", current_order[3], recipe["compound"])

                    


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