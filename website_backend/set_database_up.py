#first file
import mysql.connector as mysql
from tabulate import tabulate
from credentials import return_credentials

credentials = return_credentials()

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

# get the db cursor
cursor = db_connection.cursor()

#get the database information
cursor.execute("select database();")
database_name = cursor.fetchone()
print("[+] You are connected to the database:", database_name)

#create a new database called foodBot
cursor.execute("create database if not exists foodBot")

#use that database
cursor.execute("use foodBot")
print("[+] Change to `foodBot` database")

#create a table
cursor.execute("""create table if not exists orders (
    `id` integer primary key auto_increment not null,
    `user` varchar(255) not null,
    `time_to_be_finished` DATETIME,
    `food_type` varchar(255) not null,
    `food_amount` integer(13) not null,
    `time_ordered` DATETIME
)""")
print("[+] Table `orders` created")

# close the cursor
cursor.close()
# close the DB connection
db_connection.close()