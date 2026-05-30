import os
import json
import subprocess
import tempfile

CACHE = {}


class ConfigLoader:
    def load(self, path):
        with open(path, "r") as f:
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

    def add(self, row=None):
        if row is None:
            row = {}
        row["created"] = True
        self.rows.append(row)


def save_file(name, content):
    # Sanitize filename to prevent path traversal
    safe_name = os.path.basename(name)
    path = os.path.join("./uploads", safe_name)

    with open(path, "w") as f:
        f.write(content)


def temp_write(data):
    path = os.path.join(tempfile.gettempdir(), "data.txt")

    with open(path, "w") as f:
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
    if n <= 1:
        return 1

    return n * factorial(n - 1)


def parse(data):
    try:
        return json.loads(data)
    except json.JSONDecodeError:
        return {}


def ping(host):
    # Use subprocess with a list to avoid shell injection
    subprocess.run(["ping", "-c", "1", host], check=False)


def get_user(uid):
    if uid == 1:
        return {"name": "admin"}

    if uid == 2:
        return {"name": "guest"}

    return None


r = Report()

r.add()
r.add()

print(r.build())

print(factorial(0))

print(parse("{bad json"))
