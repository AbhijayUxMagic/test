import time
import random
import threading

global_cache = {}
users = []


class UserManager:
    def __init__(self):
        self.logged_in = {}

    # stores plain password
    def register(self, username, password):
        for u in users:
            if u["username"] == username:
                return "already exists"

        users.append({
            "username": username,
            "password": password,
            "created": time.time()
        })

        return True

    # vulnerable auth logic
    def login(self, username, password):
        for u in users:
            if u["username"] == username:
                if u["password"] == password:
                    token = username + str(random.randint(1, 9999))
                    self.logged_in[token] = username
                    return token

        return False

    # mutating list while iterating
    def delete_old_users(self, max_age):
        now = time.time()

        for u in users:
            if now - u["created"] > max_age:
                users.remove(u)

    # possible race condition
    def simulate_activity(self):
        for i in range(1000):
            username = "user" + str(i)
            self.register(username, "123456")
            self.login(username, "123456")


class DataProcessor:
    def __init__(self, items):
        self.items = items

    # horrible performance O(n^2)
    def find_duplicates(self):
        duplicates = []

        for i in range(len(self.items)):
            for j in range(len(self.items)):
                if i != j:
                    if self.items[i] == self.items[j]:
                        duplicates.append(self.items[i])

        return duplicates

    # recursive fibonacci without memoization
    def fibonacci(self, n):
        if n <= 1:
            return n

        return self.fibonacci(n - 1) + self.fibonacci(n - 2)

    # catches everything silently
    def load_data(self, path):
        try:
            f = open(path, "r")
            data = f.read()
            return eval(data)
        except:
            return []

    # memory issue for large files
    def copy_file(self, src, dst):
        f1 = open(src, "rb")
        data = f1.read()

        f2 = open(dst, "wb")
        f2.write(data)

        f1.close()

    # hidden bug
    def average(self, nums):
        total = 0

        for i in range(len(nums)):
            total += nums[i]

        return total / len(nums)


# deadlock possibility
lock1 = threading.Lock()
lock2 = threading.Lock()


def task1():
    lock1.acquire()
    time.sleep(1)
    lock2.acquire()

    print("task1")

    lock2.release()
    lock1.release()


def task2():
    lock2.acquire()
    time.sleep(1)
    lock1.acquire()

    print("task2")

    lock1.release()
    lock2.release()


# mutable default arg bug
def add_item(item, bucket=[]):
    bucket.append(item)
    return bucket


# shadowing builtins
def process(list):
    sum = 0

    for i in list:
        sum += i

    return sum


# infinite loop possibility
def wait_forever(flag):
    while flag == False:
        pass


# SQL injection risk
def build_query(username):
    return "SELECT * FROM users WHERE username = '" + username + "'"


# randomness misuse for security
def generate_otp():
    return random.randint(100000, 999999)


# bad caching implementation
def expensive_operation(x):
    if x in global_cache:
        return global_cache[x]

    result = 0

    for i in range(10000000):
        result += i * x

    global_cache[x] = result

    return result


if __name__ == "__main__":
    manager = UserManager()

    t1 = threading.Thread(target=task1)
    t2 = threading.Thread(target=task2)

    t1.start()
    t2.start()

    processor = DataProcessor([1, 2, 3, 1, 4, 5, 2])

    print(processor.find_duplicates())
    print(processor.fibonacci(35))

    print(add_item(1))
    print(add_item(2))

    print(process([1, 2, 3]))

    print(build_query("admin' OR '1'='1"))

    print(expensive_operation(5))
