import random
def d4(amount=1):
    total = 0
    for i in range(amount):
        total += random.randint(1, 4)
    return total


def d6(amount=1):
    total = 0
    for i in range(amount):
        total += random.randint(1, 6)
    return total


def d8(amount=1):
    total = 0
    for i in range(amount):
        total += random.randint(1, 8)
    return total


def d10(amount=1):
    total = 0
    for i in range(amount):
        total += random.randint(1, 10)
    return total


def d12(amount=1):
    total = 0
    for i in range(amount):
        total += random.randint(1, 12)
    return total


def d20(amount=1):
    total = 0
    for i in range(amount):
        total += random.randint(1, 20)
    return total