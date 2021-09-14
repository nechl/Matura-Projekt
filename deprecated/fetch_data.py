import mysql.connector as mysql
from helping_f import helping_functions
from datetime import datetime, timedelta

from tabulate import tabulate
DEBUG_LEVEL = 0
printd = helping_functions(DEBUG_LEVEL).printd

def fetch_data(credentials): 
    print(credentials)
    #Credentials:   
    HOST = credentials["HOST"]
    DATABASE = credentials["DATABASE"]
    USER = credentials["USER"]
    PASSWORD = credentials["PASSWORD"]
    
    #connect to the database
    db_connection = mysql.connect(host=HOST, database=DATABASE, user=USER, password=PASSWORD)
    print(db_connection.get_server_info())

    cursor = db_connection.cursor()  
    
    #fetch the database
    cursor.execute("select * from orders")
    
    #get all selected rows
    rows = cursor.fetchall()
    
    #print all orders(rows) in a table with tabulate
    printd(tabulate(rows, headers=cursor.column_names),0)
    
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
    now = datetime.now() # time object

    for i in range(len(orders)):
        printd(orders[str(i)],1)
        if orders[str(i)]["time_finish"] > now:
            #print(orders[str(i)]["user"],"'s food is going to be prepared")
            pass
        elif orders[str(i)]["time_finish"] < now:
            #print(orders[str(i)]["user"],"'s food has been prepared")
            pass
    #orders contain now all orders
    print("CURRENT ORDERS:")
    print("------------------------------------------------")
    print(tabulate(orders_for_tabulate, cursor.column_names))

    cursor.close()
    db_connection.close()
    current_tuple = [orders, orders_for_tabulate]
    return current_tuple
if __name__ == "__main__":
    print("executed from beginning")
