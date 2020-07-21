import sqlite3
from sqlite3 import Error as e


#creates connection
def connect():
    conn = sqlite3.connect('Data/data_meteo.db')
    return conn

# creates cursor
def create_cursor(conn):
    c = conn.cursor()
    return c

# closes and saves connection
def commit_and_close(conn):
    conn.commit()
    conn.close()
    

# add_Data saves passed data into weather table
def add_Data(data):
    conn = connect()
    c = create_cursor(conn)
    c.executemany('INSERT INTO weather VALUES (?,?,?,?,?,?,?)', data)
    print("data added sucessfully"+"\n")
    commit_and_close(conn)




#create_table creates table weather
def create_table(conn):
    c = create_cursor(conn)
    c.execute('''CREATE TABLE weather(date text, temp real, temp_avg real , temp_min real, temp_max real , humidity real , wind_speed real)''')

#max_min_avg returns value min and max temperature from the row with the passed date and avg of all data temperature collected
def max_min_avg(date):
    min=""
    max=""
    avgFromAll = 0
    i=0
    listTemp =[]
    conn = connect()
    c = create_cursor(conn)
    for row in c.execute('SELECT * FROM weather ORDER BY date'):
        listTemp.insert(i,row[2])
        i+=1

        if row[0]==date:
            min=str(row[3])
            max=str(row[4])
            
    for x in listTemp:
        avgFromAll+=x
        
    commit_and_close(conn)
    avgFromAll/=listTemp.__len__()
    if min=="":
        return "no data for inputed date"
    else:
        return "temp min = "+min+"\n"+"temp max = "+max+"\n"+"avg = "+str(avgFromAll)+"\n"
