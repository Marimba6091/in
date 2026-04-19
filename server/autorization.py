import json
import sql.dataBase as dataBase
import datetime as dt

class Log_in:
    @staticmethod
    def log_in_cookie(cookie):
        coockie_line = cookie.split(b";")
        login = ""
        password = ""
        for i in coockie_line:
            if b" login" in i:
                login = i.split(b"=")[1].decode()
        for i in coockie_line:
            if b"password" in i:
                password = i.split(b"=")[-1].decode()
        d = f"SELECT username, email, password_, rule FROM profiles WHERE email = \'{login}\' AND password_ = \'{password}\'"
        result = dataBase.execute(d)
        if not isinstance(result, int):
            if len(result) == 1:
                return (login, True, result[0][0], result[0][3])
        return ("Guest", False, "", "guest")
    
    @staticmethod
    def log_in(email, password):
        if email and password: 
            d = f"SELECT email, password_, rule FROM profiles WHERE email = \'{email}\' AND password_ = \'{password}\'"
            result = dataBase.execute(d)
            if not isinstance(result, int):
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