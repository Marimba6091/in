import pymysql

def execute(ect):
    connection = pymysql.connect(host="localhost", port=3306, user="root", password="1111", database="dat")
    try:
        with connection.cursor() as cursor:
            cursor.execute(ect)
            fetchall = cursor.fetchall()
            connection.commit()
        return fetchall
    except Exception as e:
        pass
    return ()
