import sqlite3
from sqlite3 import Error as e



def connect():
    conn = sqlite3.connect('Data/data_meteo.db')
    return conn

def create_cursor(conn):
    c = conn.curson()
    return c

def commit_and_close(conn):
    conn.commit()
    conn.close()
    


def add_Data(data):
    conn = connect()
    c = create_cursor(conn)
    c.executemany('INSERT INTO weather VALUES (?,?,?,?,?,?,?)', data)
    print("data added sucessfully")
    conn.commit_and_close()




    
def create_table(conn):
    c = create_cursor(conn)
    c.execute('''CREATE TABLE weather IF NOT EXIST
             (date text, temp real, temp_avg real , temp_min real, temp_max real , humidity real , wind_speed real)''')


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
        return "temp min = "+min+"\n"+"temp max = "+max+"\n"+"avg = "+str(avgFromAll)
