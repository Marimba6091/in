import pymysql


connection = pymysql.connect(host="localhost", port=3306, user="root", password="1111", database="dat")

def execute(ect):
    with connection.cursor() as cursor:
        cursor.execute(ect)
        fetchall = cursor.fetchall()
        connection.commit()
    return fetchall