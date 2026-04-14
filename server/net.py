from urllib.parse import unquote, quote
import os
import datetime as dt
import json
import server.autorization as autorization
import hashlib


class Net:
    def __init__(self, chest: str, href: str):
        self.chest = chest
        self.href = href

    def date(self, str=True):
        dat = dt.datetime.now()
        return dat.isoformat(sep=" ") if str else dat

    def hasher(mes):
        hsh = hashlib.sha256(mes).digest(16)
        content = f"HTTP/1.1 200 OK\r\nContent-Type: text/txt\r\nContent-Length:{hsh}\r\nConnection: close\r\n\r\n"
        return content + hsh
    
    def printl(*args, end="\n"):
        if args[1]:
            file = open("server/logs.txt", "a", encoding="utf-8")
            file.write(f"\n{args[1]}")
            file.close()
            print(args[1])
    
    def font(self, path):
        file = open(self.chest + path, "rb")
        font = file.read()
        file.close()
        exp = path.split(".")[1]
        content = f"HTTP/1.1 200 OK\r\nContent-Type: font/{exp}\r\nContent-Length:{len(font)}\r\nConnection: close\r\n\r\n"
        content = content.encode("utf-8") + font
        return content

    def image(self, path, http=True):
        file = open(self.chest + path, "rb")
        img = file.read()
        file.close()
        exp = path.split('.')[1]
        if http:
            content = f"HTTP/1.1 200 OK\r\nContent-Type: image/{exp}\r\nContent-Length:{len(img)}\r\nConnection: close\r\n\r\n"
            content = content.encode() + img
            return content
        return img

    def text(self, path, descriptions="", add_data=(), code_ask=200):
        self.printl(descriptions, end="")
        file = open(self.chest + path, "r", encoding="utf=8")
        string = file.read()
        file.close()
        if add_data:
            for i in add_data:
                string = string.replace(i[0], i[1])
        string = string.encode("utf-8")
        content = f"HTTP/1.1 {code_ask} OK\r\nContent-Type: text/html\r\nContent-Length:{len(string)}\r\n\r\n"
        return content.encode("utf-8") + string
    
    @staticmethod
    def get_icon(exp):
        return {"jpeg": "image", "ico": "image", "jpg": "image", "html": "html", "mp3": "sound", "h": "html", "ttf": "font", "png": "image", "mp4":"video"}.get(exp, "unknown")
    
def show_content(request, adr, host):
    net = Net("data", f"http://{host[0]}/")
    lines = request.split(b"\r\n")
    method, path, http_v = lines[0].decode().split(" ")
    path = unquote(path)
    path = path.replace("//", "/")
    Dpath = path.split("/")
    net.printl(f"{path}{(60 - len(path)) * ' '}| User adress - {adr} | {net.date()} | <{method}>")
    print(request)
    if method == "POST":
        print(request)
        if len(lines) > 14:
            messege = lines[-1].decode()
            json_ = json.loads(messege)
            if json_["method"] == "log_in":
                return autorization.Log_in.log_in(json_.get("login"), json_.get("password"))
            elif json_["method"] == "hash":
                return Net.hasher(json_.get("text"))
    
    cookie = b""
    for i in lines:
        if b"Cookie: " in i:
            cookie = i
            break

    rules = autorization.Log_in.log_in_cookie(cookie)
    print("rules -", rules)
    if path == "/":
        if rules:
            return net.text("/index/index.html")
        return net.text("/index/index_log.html")
    elif os.path.isfile(net.chest + path):
        if "." in path:
            exp = Dpath[-1].split(".")[-1]
            extension = get_extensions(net, exp)
            if extension:
                return extension(path)
        return net.text(path)
    return net.text("/Error.html", descriptions="Error", add_data=((".actual_domen.", net.href),), code_ask=404)
    

def get_extensions(obj: Net, extension):
    func = {"jpeg": obj.image, "ico": obj.image, "jpg": obj.image, "html": obj.text, "ttf": obj.font, "png": obj.image}.get(extension, False)
    return func

if __name__ == "__main__":
    print("Start from file \"main.py\", please")