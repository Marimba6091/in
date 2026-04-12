from urllib.parse import unquote, quote
import os
import datetime as dt
import json
import server.autorization as autorization


class Net:
    def __init__(self, chest: str, href: str):
        self.chest = chest
        self.href = href

    def date(self, str=True):
        dat = dt.datetime.now()
        return dat.isoformat(sep=" ") if str else dat
    
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
    
    def listing(self, path):
        lst = {"dir":[], "file":[]}
        for i in os.listdir(path):
            if os.path.isfile(path + "/" + i):
                lst["file"] += [i]
                continue
            if os.path.isdir(path + "/" + i):
                lst["dir"] += [i]
                continue
        string = ""
        for i in lst:
            for k in lst[i]:
                add = ""
                if i == "dir":
                    string += f"<div class=\"features\">\n<a class=\"feature\" href=\"{self.href}{("listing/" + path[5:] + "/" + quote(k).replace("//", "/").replace("%28", "(").replace("%29", ")"))}\">\n<img class=\"icon\" src=\"{self.href}img/icons/folder.png\">\n<p>{k}</p>\n</a>\n</div>\n"
                else:
                    if k.split(".")[-1] == "mp3":
                        add = f"<a class=\"feature-play\" href=\"{self.href}media.html?&{quote(path[5:]) + "/" + k}\"><img class=\"icon\" src=\"{self.href}img/icons/play.png\"></a>\n"
                    string += f"<div class=\"features\">\n<a class=\"feature\" href=\"{self.href}{(path[5:] + "/" + quote(k).replace("%28", "(").replace("%29", ")"))}\">\n<img class=\"icon\" src=\"{self.href}img/icons/{self.get_icon(k.split(".")[-1])}.png\">\n<p><p>{k.replace("%20", " ")}</p>\r\n</a>{add}\n</div>\n"
        file = open(self.chest + "/listing.html", "r", encoding="utf-8")
        content = file.read()
        file.close()
        content = content.replace(".add_data.", string).replace(".title.", path)
        content = content.encode("utf-8")
        http_ask = f"HTTP/1.1 200 OK\nContent-Type: text/html\nContent-Length:{len(content)}\n\n"
        content = http_ask.encode("utf-8") + content
        return content
    
    @staticmethod
    def get_icon(exp):
        return {"jpeg": "image", "ico": "image", "jpg": "image", "html": "html", "mp3": "sound", "h": "html", "ttf": "font", "png": "image", "mp4":"video"}.get(exp, "unknown")
    
def show_content(request, adr, host):
    net = Net("data", f"http://{host[0]}/")
    get_req = request
    lines = get_req.split(b"\r\n")
    method, path, http_v = lines[0].decode().split(" ")
    path = unquote(path)
    path = path.replace("//", "/")
    rules = autorization.Log_in.authenticator(adr)
    Dpath = path.split("/")
    net.printl(f"{path}{(60 - len(path)) * ' '}| User adress - {adr} | {net.date()} | <{method}>")
    if method == "POST":
        if len(lines) > 14:
            messege = lines[14].decode()
            json_ = json.loads(messege)
            if json_["method"] == "log_in":
                return autorization.Log_in.log_in(json_, adr)
    if path == "/":
        if rules:
            return net.text("/index/index.html")
        return net.text("/index/index_log.html")
    elif "listing" == Dpath[0]:
        if rules == ("admin"):
            path = "data/" + "/".join(Dpath[1:])
            if os.path.isdir(path):
                return net.listing(path)
        else:
            return net.text("/authenticator.html")
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