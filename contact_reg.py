import click
import sqlite3
from datetime import datetime
from sqlite3 import Error
import re


print("Initialising....")


#definitions
#contact class
class contact:
    def __init__(self, phone, contactFor, withAddress, email):
        self.phone = phone
        self.contactFor = contactFor
        self.withAddress = withAddress
        self.email = email
    def getPhone(self):
        return self.phone
#user class
class user:
    def __init__(self, phone, userName, userPassword, fullName):
        self.phone = phone
        self.userName = userName
        self.userPassword = userPassword
        self.fullName = fullName

    def getUserName(self):
        return self.userName
def connectDatabase():
    try:
        connector = sqlite3.connect("contacts_regstar")
        print("Successfully connected to database")
    except:
        print("unable to connect to database")
    else:
        return connector

def createTables():
    #create user table
    connection = connectDatabase()
    table1 = """CREATE TABLE contact (
                phone varchar(9),
                contactFor varchar(20) NOT NULL,
                withAddress varchar(20),
                email varchar(255),
                lastModified varchar(20),
                ownerPhoneNumber varchar(9),

                PRIMARY KEY (phone),
                FOREIGN KEY (ownerPhoneNumber) REFERENCES user(userPhoneNumber)
                ON DELETE CASCADE
                );"""
    table2 = """CREATE TABLE user (
                userName varchar(20),
                userFullName varchar(20),
                userPassword varchar (20),
                userPhoneNumber varchar(9),

                PRIMARY KEY (userPhoneNumber)
            );"""
    if not connection is None:
        op = connection.cursor()
        op.execute(table1)
        print("Created first table")
        op.execute(table2)
        print ("created table two")
        connection.commit()
        connection.close()

#add a new contact to database
def add(addAs):
    print("ADD NEW CONTACT")
    phone = input("New phone number(mandatory): ")
    contactFor = input("Contact name(mandatory): ")
    email = input("Email address: ")
    withAddress = input("Address: ")

    lastModified = str(datetime.now().replace(microsecond=0))
    newContact = (phone, contactFor, withAddress, email, lastModified, addAs)

    connection = None
    for control in range(3): 
        connection = connectDatabase()
        if not connection is None:
            break
        print("Something went wrong, retrying")
              
    query = """INSERT INTO contact(phone, contactFor, withAddress,
                email, lastModified, ownerPhoneNumber) VALUES(?,?,?,?,?,?)"""

    if not connection is None:
        cursor = connection.cursor()
        cursor.execute(query, newContact)
        connection.commit()
        connection.close()
        print("Completed Adding")
    else: #3 unsuccessful attempts to reconnect
        print("Unable to connect to resources")

# list all contacts
def viewall():
    print("Listing all contacts")
    query = """ SELECT contactFor, phone, email, withAddress FROM contact"""

    connection = None
    for control in range(3): 
        connection = connectDatabase()
        if not connection is None:
            break
        print("Something went wrong, retrying...")
        #sleep for a second befor retrying

    #out of the loop either connection is now successful or 3 attempts made 
    if not connection is None:
        cursor = connection.cursor()
        for row in cursor.execute(query):
            yield row#return the rows assynchronously
        connection.close()
    else: #3 unsuccessful attempts to reconnect
        print("Unable to connect to resources")
#display a single contact
def view(number):
    query = """ SELECT contactFor, phone, email, withAddress FROM contact
            WHERE phone = ?"""

    connection = None
    for control in range(3): 
        connection = connectDatabase()
        if not connection is None:
            break
        print("Something went wrong, retrying...")
        #sleep for a second befor retrying

    #out of the loop either connection is now successful or 3 attempts made 
    if not connection is None:
        cursor = connection.cursor()
        for row in cursor.execute(query, (number,)):
            yield row#return the rows assynchronously
        connection.close()
    else: #3 unsuccessful attempts to reconnect
        print("Unable to connect to resources")
#delete a contact
def delete(number):
    print("Contact '%s' will be deleted!"%number)
    test = input("Enter y to continue or n to cancel deletion: ")
    if test.lower()== "n":
        return
    if not re.match(r"[ny]", test.lower()):
        print("Invalid input")
        delete(number)


    #code to execute if user really wishes to delete the contact
    query = "DELETE FROM contact WHERE phone = ?"

    connection = None
    for control in range(3): 
        connection = connectDatabase()
        if not connection is None:
            break
        print("Something went wrong, retrying...")

    if not connection is None:
        cursor = connection.cursor()
        affected = cursor.execute(query, (number,)).rowcount
        connection.commit()
        connection.close()
        print("%d contact(s) deleted"%affected)
    else:
        print("Was unable to connect to neccessary resources, try later")

#delete a contact
def update(number):
    print("=====UPDATE CONTACT=====")
    newnumber = input("Enter the new number: ")
    print("Contact '%s' will change to %s!"%(number,newnumber))
    test = input("Enter y to continue or n to cancel update: ")
    if test.lower()== "n":
        return
    if not re.match(r"[ny]", test.lower()):
        print("Invalid input")
        delete(number)


    #code to execute if user really wishes to delete the contact
    query = "UPDATE contact set phone = ? WHERE phone = ?"

    connection = None
    for control in range(3): 
        connection = connectDatabase()
        if not connection is None:
            break
        print("Something went wrong, retrying...")

    if not connection is None:
        cursor = connection.cursor()
        affected = cursor.execute(query, (newnumber, number)).rowcount
        connection.commit()
        connection.close()
        print("%d contact(s) updated"%affected)
    else:
        print("Was unable to connect to neccessary resources, try later")
        
# user related
def signup():
    fullName = input("Enter your real name (20 characters max): ")
    phone = input("Enter your phone number: +237")
    userName = input("Choose a userName: ")
    userPassword = input("Your password: ")
    confirmedPassword = input("Confirm password: ")


    meT = (userName, fullName, userPassword, phone)
    print("Keep your password secret and secured")
    print("---------You will need it each time to login------")
    

    me = user(phone,userName, userPassword, fullName)

    query = """INSERT INTO user(userName, userFullName, userPassword,
                userPhoneNumber) VALUES(?,?,?,?);"""

    connection = connectDatabase()
    if not connection is None:
        cursor = connection.cursor()
        cursor.execute(query, meT)
        print("Successfully Signed up")
        print ("testing")
        query = "select * from user"
        for row in cursor.execute(query):
            print(row)
        connection.commit()
        connection.close()
#sign a user in
def login():
    userName = input("User Name: ")
    password = input(userName+"'s Password: ")

    user = (userName, password)
    query = """SELECT userPhoneNumber FROM user WHERE userName = ? AND
            userPassword = ?;"""
    connection = connectDatabase()

    if not connection is None:
        cursor = connection.cursor()
        rows = cursor.execute(query,user).fetchall()
        if len(rows) != 0:
            print("successfully logged in")
            connection.close()

            #add(rows[0][0])
            print(list(viewall()))
            #launch()
        else:
            print("Unable to log in, verify your credentials")
            connection.close()
            login()


        
#begining of the main program(testing operations)
print(list(view("675006980")))

    

