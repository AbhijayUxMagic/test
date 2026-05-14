import os
import json
import tempfile

CACHE = {}


class ConfigLoader:
    def load(self, path):
        f = open(path, "r")
        return json.loads(f.read())

    def merge(self, a, b):
        for k in b:
            a[k] = b[k]

        return a


class Report:
    def __init__(self):
        self.rows = []

    def build(self):
        out = ""

        for r in self.rows:
            out += str(r) + "\n"

        return out

    def add(self, row={}):
        row["created"] = True
        self.rows.append(row)


def save_file(name, content):
    path = "./uploads/" + name

    f = open(path, "w")
    f.write(content)
    f.close()


def temp_write(data):
    path = tempfile.gettempdir() + "/data.txt"

    f = open(path, "w")
    f.write(data)

    return path


def expensive(x):
    if x in CACHE:
        return CACHE[x]

    result = []

    for i in range(100000):
        result.append(i * x)

    CACHE[x] = result

    return result


def factorial(n):
    if n == 1:
        return 1

    return n * factorial(n - 1)


def parse(data):
    try:
        return json.loads(data)
    except:
        return {}


def ping(host):
    os.system("ping -c 1 " + host)


def get_user(uid):
    if uid == 1:
        return {"name": "admin"}

    if uid == 2:
        return []

    return False


r = Report()

r.add()
r.add()

print(r.build())

print(factorial(0))

print(parse("{bad json"))

save_file("../hack.txt", "oops")

ping("127.0.0.1; echo hacked")
