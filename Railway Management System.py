import mysql.connector
from tabulate import tabulate
import configparser
import os
import time

config = configparser.ConfigParser()

if os.path.exists("config.txt")!=True:
    config['Checks'] = {
    'table_exists': 'False',
    }
    config['Creds'] = {
        'username': '',
        'password': '',
    }

    # Write to config.txt
    with open('config.txt', 'w') as configfile:
        config.write(configfile)

config.read('config.txt')

if config['Creds']['username'] == '' and config['Creds']['password'] == '':
    os.system('cls')
    print("\n*************************************************************************")
    print("                     RAILWAY MANAGEMENT SYSTEM         ")
    print("\nMySQL Login:\n")
    sqlname=input("Username: ")
    sqlpass=input("Password: ")
    quesave=input("Enable auto-login? (Y/N): ")
    try:
        conn = mysql.connector.connect(host='localhost',user=sqlname,passwd=sqlpass)
        os.system('cls')
    except:
        print("Username or password does not exists.")
        exit()
    if quesave=="Y" or quesave=="y":
        config['Creds']['username']=sqlname
        config['Creds']['password']=sqlpass
        with open('config.txt', 'w') as configfile:
            config.write(configfile)
else:
    sqlname=config['Creds']['username']
    sqlpass=config['Creds']['password']
    os.system('cls')

try:
    conn = mysql.connector.connect(host='localhost',user='root',passwd=sqlpass,database='railway_management')
    mycursor = conn.cursor()
except mysql.connector.errors.ProgrammingError:
    conn = mysql.connector.connect(host='localhost',user='root',passwd=sqlpass)
    mycursor = conn.cursor()
    mycursor.execute("CREATE DATABASE railway_management")
    conn.commit()


if conn.is_connected():
    print('Successfully Connected!')
else:
    print('Not connected')

#PNR is the abbreviation of "Passenger Name Record" and
# it is also used as a booking number
def create_passengers():
    if config['Checks']['table_exists']!='True':
        try:
            query = 'Create table if not exists passengers\
                    (\nPname varchar(30) not null,\
                    Age integer(25),\
                    Trainno integer(20),\
                    No_of_pass integer(25),\
                    Class varchar(15),\
                    Destination varchar(30),\
                    Amount integer(20),\
                    Status varchar(25),\
                    Pnrno varchar(20))'
            mycursor.execute(query)
            print('\nTable Passengers created')
            config['Checks']['table_exists'] = "True"
            with open('config.txt', 'w') as configfile:
                config.write(configfile)
        except:
            print('\nERROR FOUND')
    else:
        print('You created a table previously.')


def add_passengers():
    try:
        while True:
            Pname = input("\nENTER PASSENGER NAME : ")
            Age = int(input("ENTER PASSENGER AGE : "))
            Trainno = int(input("ENTER TRAIN NO. : "))
            No_of_pass = int(input("ENTER NO. OF PASSENGERS : "))
            Class = input("ENTER CLASS TO TRAVEL IN : ")
            Destination = input("ENTER THE DESTINATION : ")
            Amount = int(input("ENTER FARE : "))
            Status = input("ENTER STATUS : ")
            Pnrno = input("ENTER PNR NO. : ")
            query = f"insert into passengers values('{Pname}',{Age},{Trainno},{No_of_pass},'{Class}','{Destination}',{Amount},'{Status}','{Pnrno}')"
            mycursor.execute(query)
            ans = input('\nDo you want to enter more records(y/n)? : ')
            if ans.lower() in 'Nn':
                break
        conn.commit()
        print('\nRecord of Passenger Inserted')
    except:
        print('\nERROR FOUND')
            

def create_trainsdetail():
    try:
        query2 = 'Create table if not exists trainsdetail\
                  (\nTname varchar(30),\
                   Tnum integer primary key,\
                   Source varchar(30),\
                   Destination varchar(30),\
                   Fare integer(20),\
                   Ac1 varchar(25),\
                   Ac2 varchar(30),\
                   Sleeper varchar(25))'
        mycursor.execute(query2)
        print('\nTable Trains Detail Created')
    except:
        print('\nERROR FOUND')


def add_trainsdetail():
    try:
        while True:
            Tname = input("\nENTER TRAIN NAME : ")
            Tnum = int(input("ENTER TRAIN NUMBER : "))
            Source = input("ENTER SOURCE OF TRAIN : ")
            Destination = input("ENTER DESTINATION OF TRAIN : ")
            Fare = int(input("ENTER FARE OF STATION : "))
            Ac1 = input("ENTER NO. OF SEATS FOR AC1 : ")
            Ac2 = input("ENTER NO. OF SEATS FOR AC2 : ")
            Sleeper = input("ENTER NO. OF SEATS FOR SLEEPER : ")
            query2 = f"insert into trainsdetail values('{Tname}',{Tnum},'{Source}','{Destination}',{Fare},'{Ac1}','{Ac2}','{Sleeper}')"
            mycursor.execute(query2)
            ans = input('\nDo you want to enter more records(y/n)? : ')
            if ans.lower() in 'Nn':
                break
        conn.commit()
        print('\nRecord inserted in Trains Detail')
    except:
        print('\nERROR FOUND')


def showpassengers():
    print('\nALL PASSENGERS DETAIL ARE AS FOLLOWS','\n')
    qry = f"select * from passengers" 
    mycursor.execute(qry)
    mypass = mycursor.fetchall()
    c = mycursor.rowcount
    h = ['Pname','Age','Train No','No of Pass','Class','Destination','Amount','Status','PNRNo']
    print(tabulate(mypass,headers = h,tablefmt = 'fancy_grid'))


def showtrainsdetail():
    print('\nALL TRAINS DETAIL ARE AS FOLLOWS','\n')
    qry = f"select * from trainsdetail" 
    mycursor.execute(qry)
    mytraindetail = mycursor.fetchall()
    c = mycursor.rowcount
    h = ['Train Name','Train No','Source','Destination','Fare','AC1','AC2','Sleeper']
    print(tabulate(mytraindetail,headers = h,tablefmt = 'fancy_grid'))


def disp_pnrno():
    showpassengers()
    try:
        pnrno = input('\nEnter PNRno : ')
        qry = f"select Pname,Status from passengers where Pnrno = '{pnrno}'" 
        mycursor.execute(qry)
        mypnrno = mycursor.fetchall()
        c = mycursor.rowcount
        h = ['Pname','Status']
        if c == 0:
            print('\nThe PNR number you are looking for is not found !!')
        else:
            print(tabulate(mypnrno,headers = h,tablefmt = 'fancy_grid'))      
    except :
        print('\nERROR FOUND')


def ticketreservation():
    print('\nGOA EXPRESS TO NEW DELHI : ')
    print()
    print('1. FIRST CLASS AC RS 6000 per PERSON')
    print('2. SECOND CLASS AC RS 5000 per PERSON')
    print('3. THIRD CLASS AC RS 4000 per PERSON')
    print('4. SLEEPER CLASS RS 3000 per PERSON')
    x = int(input('\nENTER YOUR CHOICE OF TICKET PLEASE : '))
    n = int(input('HOW MANY TICKETS YOU NEED ? : '))

    if(x==1):
        print('\nYOU HAVE CHOSEN FIRST CLASS AC TICKET')
        s = 6000*n
    elif(x==2):
        print('\nYOU HAVE CHOSEN SECOND CLASS AC TICKET')
        s = 5000*n
    elif(x==3):
        print('\nYOU HAVE CHOSEN THIRD CLASS AC TICKET')
        s = 4000*n
    elif(x==4):
        print('\nYOU HAVE CHOSEN SLEEPER TICKET')
        s = 3000*n
    else:
        print('\nINVALID OPTION !!')
        print('\nPLEASE CHOOSE A TRAIN')
    print('\nYour TOTAL TICKET PRICE is : ',s,'\n')

def cancel():
    showpassengers()
    try:
        pnrno = input('\nEnter the PNR No. for which you want to cancel the ticket : ')
        cancel = f"Delete from passengers where Pnrno = '{pnrno}'"
        mycursor.execute(cancel)
        mypnrno = mycursor.fetchall()
        c = mycursor.rowcount
        conn.commit()
        if c == 0:
            print('\nThe PNR number you are looking for is not found !!')
        else:
            print('\nYOUR TICKET RESERVATION HAS BEEN CANCELLED')
    except:
        print('\nERROR FOUND')

def reset_config():
    config['Checks']['table_exists'] = "False"
    config['Creds']['username']=''
    config['Creds']['password']=''
    with open('config.txt', 'w') as configfile:
        config.write(configfile)
    print("Reset was complete.")
# MAIN PROGRAM
while True:
    time.sleep(1)
    os.system('cls')
    print("\n*************************************************************************")
    print("                     RAILWAY MANAGEMENT SYSTEM         ")
    print("\nPRESS     FOR")
    count=1
    with open('titles.txt','r') as disp:
        for l in disp:
            if count<=9:
                print("  "+str(count)+".      "+l, end='')
            else:
                print(" "+str(count)+".      "+l, end='')
            count+=1
    opt = int(input('\nEnter your choice : '))
    if opt==1:
        os.system('cls')
        create_passengers()
    elif opt==2:
        os.system('cls')
        add_passengers()
    elif opt==3:
        os.system('cls')
        create_trainsdetail()
    elif opt==4:
        os.system('cls')
        add_trainsdetail()
    elif opt==5:
        os.system('cls')
        showpassengers()
    elif opt==6:
        os.system('cls')
        showtrainsdetail()
    elif opt==7:
        os.system('cls')
        disp_pnrno()
    elif opt==8:
        os.system('cls')
        ticketreservation()
    elif opt==9:
        cancel()
    elif opt==10:
        os.system('cls')
        reset_config()
    elif opt==11:
        os.system('cls')
        print('\nTHANKYOU\n')
        break    
    else:
        os.system('cls')
        print('\nWRONG CHOICE TRY AGAIN')
        continue


    
