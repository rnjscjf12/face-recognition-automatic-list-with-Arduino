import pymysql
import time

conn = None
cur = None

dateDB = ""
nameDB = ""
temperateDB = ""

sql = ""

timeStamp = time.time()
tm = time.localtime(timeStamp)
timeString = time.strftime('%Y-%m-%d %H:%M:%S')

conn = pymysql.connect(host="127.0.0.1", user="root", password="root", db="capstonedesign", charset="utf8")  # 1. DB 연결
cur = conn.cursor() # 2. 커서 생성 (트럭, 연결로프)

dateDB = timeString
nameDB = str('전준형')


sql = "INSERT INTO 명부 VALUES('"+dateDB+"','"+nameDB+"','36.5')"
cur.execute(sql)
conn.commit()
    
conn.close()    
