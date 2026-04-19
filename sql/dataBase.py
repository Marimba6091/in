import pymysql
import time
import random

def execute(ect):
    connection = pymysql.connect(host="localhost", port=3306, user="root", password="1111", database="dat")
    for i in range(5):
        try:
            with connection.cursor() as cursor:
                cursor.execute(ect)
                fetchall = cursor.fetchall()
                connection.commit()
            return fetchall
        except Exception as e:
            if e.args[0] == 2013:
                time.sleep(random.randint(1, 10) / 100)
            else:
                break
    return 0
