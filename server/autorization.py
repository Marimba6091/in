import json
import sql.dataBase as dataBase
import datetime as dt

class Log_in:
    @staticmethod
    def authenticator(adr):
        file = open("authenticator.json", "r")
        dct = json.load(file)
        file.close()
        if dct:
            for step in dct:
                for i in range(len(dct[step])):
                    dat = dt.datetime.now() - dt.datetime.fromisoformat(dct[step][i][1])
                    if dat.seconds // 60 > 10:
                        file = open("authenticator.json", "w")
                        dct[step].pop(i)
                        json.dump(dct, file)
                        file.close()
        for i in dct["log_in"]:
            if adr[0] == i[0]:
                return True
        return False
    
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

    @staticmethod
    def log_in(data, adr):
        email = data.get("login", "")
        password = data.get("password", "")
        d = f"SELECT email, password_ FROM profiles WHERE email = \'{email}\' AND password_ = \'{password}\'"
        result = dataBase.execute(d)
        if result:
            Log_in.authenticator("0.0")
            file = open("authenticator.json", "r")
            dct = json.load(file)
            file.close()
            if dct:
                dct["log_in"] += [[adr[0], dt.datetime.now().isoformat(sep=" ")]]
                file = open("authenticator.json", "w")
                json.dump(dct, file)
                file.close()
                return Log_in.return_succes(True)
        return Log_in.return_succes(False)
        