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
    cursor.execute("SELECT * FROM `orders` ORDER BY `orders`.`time_to_be_finished` ASC")
    #get all selected rows
    rows = cursor.fetchall()
    orders={}
    orders_for_tabulate = []
    for i in range(len(rows)):
        order = {"user":rows[i][1], "time_finish":rows[i][2], "food_type":rows[i][3], "food_amount":rows[i][4], "time_ordered":rows[i][5]}
        if order["time_finish"] > datetime.now():

            orders[str(len(orders))] = order #if it is the first element added(0 elements present) it HAS to be the zeroth element for processing
            orders_for_tabulate.append(rows[i])
        else:
            pass

    printd((order["user"], order["time_finish"], order["food_type"], order["food_amount"], order["time_ordered"]),1)
    printd(orders,1)
    
    for i in range(len(orders)):
        printd(orders[str(i)],1)
        if orders[str(i)]["time_finish"] > now:
            pass
        elif orders[str(i)]["time_finish"] < now:
            pass
    
    print(orders_for_tabulate)
   

    cursor.close()
    db_connection.close()
    return orders_for_tabulate


now = datetime.now()
print("[+]",now.strftime("%d.%m.%Y, %H:%M"))

try:
    while True:
        current_time = datetime.now()
        if ((now + timedelta(minutes=1)).strftime("%d.%m.%Y, %H:%M")) == current_time.strftime("%d.%m.%Y, %H:%M"):
            print("[+]Two minutes passed, prepare to fetch new orders")
            orders_old_format = fetch_data()
            print(tabulate(orders_old_format, headers=cursor.column_names))
            
            for order in orders_old_format:
                current_order = order
                
                for recipe in recipe_data["recipe"]:  
                    if current_order[3] == recipe["compound"]:
                        water_factor = current_order[4] / 1000
                        water_amount = water_factor * recipe["water_amount_per_1000_g"]
                        print("We have to cook ",current_order[4],"g of: ", current_order[3], "which is going to take: ", recipe["time_in_water"],"min in ", water_amount ,"ml of water")
                        IMPORTANT_DATA = {"what": current_order[3],"amount": current_order[4], "amount_water":water_amount,"time":current_order[2], "duration":recipe["time_in_water"]}
                        print(IMPORTANT_DATA)
                        starting_time = IMPORTANT_DATA["time"] - timedelta(minutes = IMPORTANT_DATA["duration"])
                        print(starting_time)
                        
                        if now >= starting_time:
                            print("i have to cook")

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