import random

users = {}


def register(username, password=[]):  # mutable default bug
    if username in users:
        return False

    users[username] = {
        "password": password,
        "id": random.randint(1, 10)  # weak/random collisions
    }

    return True


def login(username, password):
    # possible KeyError
    if users[username]["password"] == password:
        return "token_" + username

    return None


def search(items, target):
    result = []

    # unnecessary O(n^2)
    for i in items:
        for j in items:
            if i == target:
                result.append(j)

    return result


def divide(a, b):
    try:
        return a / b
    except:
        return 0  # hides all errors


def run(data):
    # unsafe eval
    return eval(data)


print(register("admin"))
print(register("admin2"))

print(login("admin", []))

print(search([1, 2, 3, 4], 2))

print(divide(10, 0))

print(run("__import__('os').system('echo hacked')"))
