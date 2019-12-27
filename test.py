import pyodbc

conn_str = (
    r'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};'
    r'DBQ=C:/Users/Ryan/Downloads/surazh/surazh/database2.mdb;'
    )
connection = pyodbc.connect(conn_str)

cursor = connection.cursor()

sql = "Insert into table1 (ID, SignalNumber, Language0, Language1) values (17, 'Peter','Jackson','DD')"

cursor.execute(sql)

connection.commit()