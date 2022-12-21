import mysql.connector as mcon
pswd = input("Enter password: ")
db_name = input("Enter database name: ")
mcon1=mcon.connect(host='localhost',user='root',passwd=pswd,database=db_name)
cursor=mcon1.cursor()
cursor.execute("drop database {}".format(db_name))
