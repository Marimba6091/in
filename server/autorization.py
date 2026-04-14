import json
import sql.dataBase as dataBase
import datetime as dt

class Log_in:
    @staticmethod
    def log_in_coockie(coockie):
        if b"\r\n" in coockie:
            print(coockie)
            email, password = coockie.decode().split("\r\n")
            d = f"SELECT email, password_ FROM profiles WHERE email = \'{email}\' AND password_ = \'{password}\'"
            result = dataBase.execute(d)
            if len(result) == 1:
                return True
        return False
    
    @staticmethod
    def log_in(email, password):
        if email and password: 
            d = f"SELECT email, password_ FROM profiles WHERE email = \'{email}\' AND password_ = \'{password}\'"
            result = dataBase.execute(d)
            if len(result) == 1:
                return Log_in.return_succes(True)
        return Log_in.return_succes(False)
    
    @staticmethod
    def return_succes(x):
        file = open("succes.json", "r", encoding="utf-8")
        content = file.read()
        file.close()
        if x:
            r = content.replace("\"$\"", "1").encode()
        else:
            r = content.replace("\"$\"", "0").encode()
        typ = f"HTTP/1.1 200 OK\r\nContent-Type: application/json\r\nContent-Length:{len(r)}\r\nConnection: close\r\n\r\n".encode()
        return typ + r