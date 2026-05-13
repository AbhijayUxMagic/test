# Small intentionally problematic script for testing code review systems

import threading
import time

data = []
balance = 1000


# race condition
def withdraw(amount):
    global balance

    if balance >= amount:
        current = balance
        time.sleep(0.01)
        balance = current - amount


# memory growth issue
def collect_logs():
    while True:
        data.append("log entry")


# hidden bug
def average(nums):
    total = 0

    for n in nums:
        total += n

    return total / len(nums)


# mutable default argument
def add_tag(tag, tags=[]):
    tags.append(tag)
    return tags


# broad exception catch
def parse_int(x):
    try:
        return int(x)
    except:
        return -1


# inefficient duplicate finder
def duplicates(items):
    out = []

    for i in items:
        if items.count(i) > 1:
            out.append(i)

    return out


t1 = threading.Thread(target=withdraw, args=(700,))
t2 = threading.Thread(target=withdraw, args=(700,))

t1.start()
t2.start()

t1.join()
t2.join()

print(balance)

print(add_tag("python"))
print(add_tag("bug"))

print(average([]))

print(parse_int(None))

print(duplicates([1, 2, 2, 3, 3, 3]))
