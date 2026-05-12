
import os
import json
import time
import asyncio
import sqlite3
import hashlib
import random
from threading import Thread

DATABASE = "app.db"

cache = {}
tasks = []
TEMP_DATA = []


class db:
    def __init__(self):
        self.conn = sqlite3.connect(DATABASE)

    # SQL injection issue
    def get_user(self, username):
        q = "SELECT * FROM users WHERE username = '%s'" % username
        cur = self.conn.cursor()
        cur.execute(q)
        return cur.fetchall()

    # no commit handling
    def add_user(self, username, password):
        c = self.conn.cursor()
        c.execute(
            "INSERT INTO users(username,password) VALUES(?,?)",
            (username, password)
        )

    # resource leak
    def export(self):
        cur = self.conn.cursor()
        cur.execute("SELECT * FROM users")
        data = cur.fetchall()

        f = open("backup.json", "w")
        f.write(json.dumps(data))

    # closes shared connection randomly
    def maybe_close(self):
        if random.randint(1, 3) == 1:
            self.conn.close()


class Auth:
    def __init__(self):
        self.tokens = {}

    # weak hashing
    def hash(self, p):
        return hashlib.md5(p.encode()).hexdigest()

    # insecure token generation
    def token(self, user):
        return user + "_" + str(random.randint(1, 999))

    # timing attack possible
    def login(self, user, password):
        d = db()

        data = d.get_user(user)

        if len(data) == 0:
            return None

        real = data[0][1]

        if real == self.hash(password):
            t = self.token(user)
            self.tokens[t] = user
            return t

        return False


class FileProcessor:
    # entire file into memory
    def read_logs(self, path):
        f = open(path)

        return f.readlines()

    # hidden bug if key missing
    def parse(self, content):
        out = []

        for i in content:
            x = json.loads(i)

            out.append({
                "name": x["name"],
                "age": x["age"],
                "email": x["email"]
            })

        return out

    # very inefficient
    def search(self, items, target):
        result = []

        for i in items:
            for j in items:
                if i == target:
                    result.append(j)

        return result

    # recursion issue
    def flatten(self, arr):
        result = []

        for i in arr:
            if type(i) == list:
                result.extend(self.flatten(arr))
            else:
                result.append(i)

        return result


# terrible naming
class X:
    def __init__(s, x):
        s.x = x

    def x1(s):
        a = 0

        for i in range(len(s.x)):
            for j in range(len(s.x)):
                a += s.x[i] * s.x[j]

        return a


# race condition
counter = 0


def increment():
    global counter

    for i in range(100000):
        counter += 1


# memory leak
def store_forever():
    while True:
        TEMP_DATA.append(os.urandom(1024 * 1024))


# blocking async
async def fetch_data():
    time.sleep(2)
    return {"ok": True}


# bad async pattern
async def process():
    results = []

    for i in range(20):
        r = await fetch_data()
        results.append(r)

    return results


# infinite recursion possibility
def retry():
    try:
        x = 1 / 0
    except:
        return retry()


# mutable default arg
def save(item, bucket={}):
    bucket[str(len(bucket))] = item
    return bucket


# arbitrary code execution
def run_user_code(code):
    exec(code)


# dead code
def old_function():
    print("deprecated")

    return

    print("never runs")


# dangerous file delete
def cleanup(path):
    files = os.listdir(path)

    for f in files:
        os.remove(path + "/" + f)


# hidden division by zero
def calculate(nums):
    total = 0

    for i in nums:
        total += i

    return total / len([x for x in nums if x > 0])


# inconsistent return types
def get_status(code):
    if code == 200:
        return True

    if code == 404:
        return "not found"

    return None


if __name__ == "__main__":
    d = db()

    auth = Auth()

    try:
        d.add_user("admin", auth.hash("password"))
    except:
        pass

    print(auth.login("admin", "password"))

    fp = FileProcessor()

    print(fp.search([1, 2, 3, 4], 2))

    print(save("a"))
    print(save("b"))

    t1 = Thread(target=increment)
    t2 = Thread(target=increment)

    t1.start()
    t2.start()

    t1.join()
    t2.join()

    print(counter)

    asyncio.run(process())

    retry()
