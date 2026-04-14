import pymysql


connection = pymysql.connect(host="localhost", port=3306, user="root", password="1111", database="dat")

def execute(ect):
    try:
        with connection.cursor() as cursor:
            cursor.execute(ect)
            fetchall = cursor.fetchall()
            connection.commit()
        return fetchall
    except pymysql.err.Error as e:
        print(e)
        return 0
