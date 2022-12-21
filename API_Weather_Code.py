import requests
import json
import time
import datetime
import geocoder
import matplotlib.pyplot as plt
import mysql.connector as mcon
import csv
import numpy as np

print()
print("Request pulled on:")
print(time.asctime())
a = datetime.date.today()

pswm = input("Please enter your mysql password for connectivity: ")
mcon=mcon.connect(host='localhost', user='root', passwd=pswm)
cursor=mcon.cursor()

x=input("Do you want the database to be created automatically (Y/N)? ")
while True:
    if x in ("Y","y"):
        while True:
            datb = input("Please enter the preferred name of the database in which the table should exist: ") 
            h = input("Are you sure that the above entered info is correct? (Y/N): ")            
            if h in ('Y','y'):
                print('Good job, moving on...')
                print()
                break
            elif h in ('N', 'n'):
                print("Give it another try!")
            else:
                print("Invalid choice, try again!")
                print()
        datn=datb.replace(" ", "_")
        cursor.execute('create database {}'.format(datn))
        cursor.execute('use {}'.format(datn))
    elif x in ("N", "n"):   
        while True:
            datb=input("Enter the name of an existing database in which you want the data to be saved: ")
            h = input("Are you sure that the above entered info is correct? (Y/N): ")        
            if h in ('Y','y'):
                print('Good job, moving on...')
                print()
                break
            elif h in ('N', 'n'):
                print("Give it another try!")
            else:
                print("Invalid choice,try again!")
                print()
        datn=datb.replace(" ", "_")
        cursor.execute('use {}'.format(datn))
    else:
        print("Invalid choice, try again!")
    break

lapi = 'INSERT GEOCODER API'
wapi = 'INSERT WEATHER API'

cursor.execute('show tables;')
st=cursor.fetchall()
while True:
    if st == [('weather_report',)]:
        print("The table already exists, nice!")
        s = 0
        break
    else:
        print("Would you like the MySQL table to be created automatically by the program?")
        print("Note: If you decline, no values will be written in the database!")
        x=input("Enter 'Y/y' to accept, or 'N/n' to decline: ")
        if x in ("Y","y"):
            cursor.execute('''create table weather_report(
            Date varchar(10) not null not null,
            Current_Temperature_CELSIUS decimal(4,2) not null,
            Feels_Like_CELSIUS decimal(4,2) not null,
            Humidity int(2) not null,
            Time varchar(5) not null,
            City varchar(15) not null)''')
            s = 0
            print()
            break
        elif x=="N" or x=="n":
                print("The table doesn't exist, no values will be written in database!!")
                s = 1
                break
        else:
            print("Please enter a valid choice")
        
cursor.reset()
if s == 0:
    if mcon.is_connected():
        print('Database Connection Succesful')
        print()
        h = input("Do you want to know the description of the table (Y/N): ")
        print()
        if h in ('Y', 'y'):
            cursor.execute("Desc weather_report")
            print('Description of Database is')
            print()
            for x in cursor.fetchall():
                print(x)
    else:
        print('Database Connection Error')

def coord(city):
    global result
    result = geocoder.opencage(city, key=lapi)
    print("")
    global lat
    global lon
    try:
        lat, lon = result.latlng[0], result.latlng[1]
        return lat, lon
    except TypeError:
        print("Enter a valid city!")

def cel(val):
    cels = round((val - 273.15), 2)
    return cels

def far(val):
    faren = round((val * (9/5) - 459.67), 2)
    return faren

def curr_weather():
    l = 3
    while l < 8:
        global city
        city = str.capitalize(input("Enter City name: "))
        city.rstrip()
        coord(city)
        if result.latlng == None:
            print("Invalid City name, try again...")
        else:
            resp = requests.get('https://api.openweathermap.org/data/2.5/weather?q={}&appid={}'
                                .format(city, wapi))
            if resp.status_code == 200:
                t = json.loads(resp.text)
                print("The coordinates of entered location are: \n", coord(city))
                print("-------------------------")
                print()
                print(":::::The Current Weather of {} is:::::".format(city))
                global temp
                global hum
                global feel
                hum = t['main']['humidity']
                temp= (cel(t['main']['temp']),far(t['main']['temp']))
                feel = (cel(t['main']['feels_like']), far(t['main']['feels_like']))
                print()
                print("■ Today's average temperature:", temp[0], '℃ ', 'or', temp[1], '℉')
                print('■ Feels Like:', feel[0], '℃', 'or', feel[1], '℉')
                print('■ Humidity:', hum, '%')
                l += 2
                break
            elif resp.status_code == 400:
                print("Client error \n trying again in", l, "seconds...")
                time.sleep(l)
                l += 1
            if l == 7:
                print("Too many errors, check your internet connection and arguments given and try again")
                break

def yest_weather():
    l = 3
    while l < 8:
        global city
        city = str.capitalize(input("Enter City name: "))
        dt = int((time.time()) - 86400)
        coord(city)
        if result.latlng == None:
            print("Invalid City name, try again...")
        else:
            resp = requests.get('https://api.openweathermap.org/data/2.5/onecall/timemachine?lat={}\
                                &lon={}&dt={}&appid={}'.format(lat, lon, dt, wapi))
            if resp.status_code == 200:
                t = json.loads(resp.text)
                print("The coordinates of entered location are: \n", coord(city))
                print("-------------------------")
                print()
                print(":::::The Yesterday's Weather of {} is:::::".format(city))
                global temp
                global feel
                global hum
                temp = (cel(t['current']['temp']), far(t['current']['temp']))
                feel = (cel(t['current']['feels_like']), far(t['current']['feels_like']))
                hum = t['current']['humidity']
                print()
                print("■ Yesterday's weather: ", temp[0], '℃', 'or', temp[1], '℉')
                print('■ Felt Like:', feel[0], '℃', 'or', feel[1], '℉')
                print('■ Humidity:', hum, '%')
                l += 2
                break
            elif resp.status_code == 400:
                print("Server error \n trying again in", l, "seconds...")
                time.sleep(l)
                l += 1
            if l == 7:
                print("Too many errors, check your internet connection and arguments given and try again")
                break

def tomm_weather():
    l = 3
    while l < 8:
        global city
        city = str.capitalize(input("Enter City name: "))
        city.rstrip()
        coord(city)
        if result.latlng == None:
            print("Invalid City name, try again...")
        else:
            resp = requests.get('https://api.openweathermap.org/data/2.5/onecall?lat={}&lon={}&appid={}'
                                .format(lat, lon, wapi))
            if resp.status_code == 200:
                t = json.loads(resp.text)
                print("The coordinates of entered location are: \n", coord(city))
                print("-------------------------")   
                print()
                print(":::::The Weather Forecast of {} is:::::".format(city))
                print()
                global temp
                global feel
                global hum
                temp = (cel(t['daily'][0]['temp']['day']), far(t['daily'][1]['temp']['day']))
                feel = (cel(t['daily'][0]['feels_like']['day']), far(t['daily'][1]['feels_like']['day']))
                hum = t['daily'][0]['humidity']
                print("■ Tomorrow's weather will be: ", temp[0], '℃', 'or', temp[1], '℉')
                print("■ It will feel like: ", feel[0], '℃', 'or', feel[1], '℉')
                print("■ Humidity will be: ", hum, '%')
                l += 2
                break
            elif resp.status_code == 400:
                print("Server error \n trying again in", l, "seconds...")
                time.sleep(l)
                l += 1
            if l == 7:
                print("Too many errors, check your internet connection and arguments given and try again")
                break

def graph():
    while True:
        g = input("Do you want forecast graph for next 7 days? (Y/N): ")
        if g in ('Y', 'y'):
            days = np.empty((0,), dtype=str)
            temps = np.empty((0,), dtype=int)
            mintemps = np.empty((0,), dtype=int)
            maxtemps = np.empty((0,), dtype=int)
            info = requests.get("https://api.openweathermap.org/data/2.5/onecall?lat={}&lon={}&appid={}"
                                .format(lat, lon, wapi))
            info = info.text
            data = json.loads(info)
            print("Enter the unit you want the graph in \n▶for CELSIUS, enter C/c. \n▶for FAHRENHEIT,\
 enter F/f.")
            while True:
                unit = input("Enter your choice (C/F): ")
                if unit in ('C', 'c'):
                    plt.ylabel("Temperature (in celsius)")
                    break
                elif unit in ('F', 'f'):
                    plt.ylabel("Temperature (in fahrenheit)")
                    break
                else:
                    print("Invalid choice try again....")
            print()
            for i in range(7):
                day = datetime.datetime.fromtimestamp(data["daily"][i]['dt']).strftime("%A")
                if unit in ('C', 'c'):
                    temp = cel(data['daily'][i]['temp']['day'])
                    mintemp = cel(data['daily'][i]['temp']['min'])
                    maxtemp = cel(data['daily'][i]['temp']['max'])
                elif unit in ('F', 'f'):
                    temp = far(data['daily'][i]['temp']['day'])
                    mintemp = far(data['daily'][i]['temp']['min'])
                    maxtemp = far(data['daily'][i]['temp']['max'])
                days = np.append(days, day)
                temps = np.append(temps, temp)
                maxtemps = np.append(maxtemps, maxtemp)
                mintemps = np.append(mintemps, mintemp)
            print("►    Here is the graph:")
            plt.xlabel("Days")
            plt.plot(days, temps, 'c', label='Average temperature', marker='o')
            plt.plot(days, maxtemps, 'r', label='Maximum temperature', marker='o')
            plt.plot(days, mintemps, 'b', label='Minimum temperature', marker='o')
            plt.title("The weather forecast of {} for next 7 days".format(city))
            plt.legend()
            plt.show()
            print()
            break
        elif g in ("n", "N"):
            print()
            print("Okay")
            print()
            break
        else:
            print("Invalid Choice, Try again...")

print()
#Display Data From Database
def data_from_database():
    cursor.execute('Select * from weather_report order by Time desc')
    n=int(input('Enter the number of past records you want to see: '))
    print()
    data=cursor.fetchmany(n)
    count=cursor.rowcount
    print(data)
    print()
    print('No of Records: ',count)
    cursor.reset()
    print()
print()        
# Display Data From Database by city
def data_from_city():
    a=input('Which city\'s record do you want to see? ')
    cursor.execute('Select * from weather_report where city="{}"'.format(a))
    data=cursor.fetchall()
    count=cursor.rowcount
    print()
    print(data)
    print()
    print('No of Records: ',count)
    print()
    cursor.reset()
print()        
# Dislplay Highest Temperature in record
def highest_Temp():
    cursor.execute('Select * from weather_report order by Current_Temperature_CELSIUS DESC')
    data=cursor.fetchmany(1)
    count=cursor.rowcount
    print(data)
    print()
    print('No of Records: ',count)
    cursor.reset()
    print()        
print()
# No of Data according to cities
def no_of_cities_data():
    cursor.execute('Select city,count(*) from weather_report group by City')
    data=cursor.fetchall()
    count=cursor.rowcount
    print(data)
    print()
    print('No of Records: ',count)
    cursor.reset()
    print()
    
y=time.strftime('%H:%M')

def insert():
    cursor.execute("INSERT INTO weather_report(Date, Current_Temperature_CELSIUS, Feels_Like_CELSIUS,\
                   Humidity, Time, City) VALUES('{}',{},{},{},'{}','{}')"
                   .format(tp1, temp[0], feel[0], hum, y,city.upper()))
    mcon.commit()
    print('(Data successfully saved in the database)')
    cursor.reset()

def insert_into_csv():
    with open("weather_data.csv", "a+", newline='') as csv_file:
        csv_handle = csv.writer(csv_file)
        csv_handle.writerow([tp1, temp[0], feel[0], hum, y, city.capitalize()])
        print("(CSV file appended)")

while True:
    print("What information do you want? \n● 1.Current weather \n● 2.Yesterday's weather\
          \n● 3.Tomorrow's weather")
    print()
    op = input("Enter your choice (1, 2 or 3): ")
    if op == '1':
        print("You chose for today's weather...")
        #global tp1
        tp1 = a.strftime("%d-%m-%y")
        print("◖Today's date is", tp1, "◗")
        curr_weather()
        print()
        if s == 0:
            insert()
            insert_into_csv()
        graph()
        break
    elif op == '2':
        print("You chose for yesterday's weather...")
        #global tp1
        tp2 = datetime.date.today() - datetime.timedelta(days=1)
        tp1 = tp2.strftime("%d-%m-%Y")
        print("◖Yesterday's date was:", tp1, '◗')
        yest_weather()
        print()
        if s == 0:
            insert()
            insert_into_csv()
        graph()
        break
    elif op == '3':
        #global tp1
        tp4=datetime.date.today() + datetime.timedelta(days=1)
        tp1 = tp4.strftime("%d-%m-%Y")
        print("You chose for tomorrow's weather...")
        print("◖The date tomorrow is:", tp1, '◗')
        tomm_weather()
        print()
        if s == 0:
            insert()
            insert_into_csv()
        graph()
        break
    else:
        print("INVALID CHOICE, Try Again...")

if s == 0:        
    while True:
        print('''If you want to see data from database, press 1
If you want to see data by city, press 2
If you want to see the number of records for each city, press 3
If you want to see highest temperature in the records, press 4
To end program, press 5''')
        x=int(input('Enter Your Choice: '))
        if x==1:
            print()
            print("The order of the columns is")
            print('Date,', 'Current_Temperature_CELSIUS,', 'Feels_Like_CELSIUS,','Humidity,',\
                  'Time,', 'City')
            data_from_database()
        elif x==2:
            data_from_city()
        elif x==3:
            no_of_cities_data()
        elif x==4:
            highest_Temp()
        elif x==5:
            print('Thank You')
            break
        else:
            print('Enter Valid Choice')            
    mcon.close()


# lat, lon for Jodhpur: 26.2389, 73.0243