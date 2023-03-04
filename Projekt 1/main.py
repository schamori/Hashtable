import pandas as pd
import os


def find_csv_files(relative_path):
    csv_files = []
    for file in os.listdir(relative_path):
        if file.endswith(".csv"):
            csv_files.append(os.path.join(relative_path, file))
    return csv_files


class Entry:
    def __init__(self, key, value):
        self.key = key
        self.value = value


class Hashtable:

    def __init__(self, size):
        self.size = size
        self.values = [0] * size

    def hash_func(self, key):
        p = 31
        ascii_code = sum([(p ** i) * ord(c) for i, c in enumerate(key)])
        return ascii_code % self.size

    def add(self, key, value):


        hash_code = self.hash_func(key)
        i = 1
        while self.values[hash_code] != 0:
            i = i**2
            hash_code = (hash_code + i) % self.size
            i += 1
        self.values[hash_code] = Entry(key, value)

    def search(self, key):
        hash_code = self.hash_func(key)
        i = 1
        while self.values[hash_code].key != key:
            i = i ** 2
            hash_code = (hash_code + i) % self.size
            if self.values[hash_code] == 0:
                raise KeyError
            i += 1
        return self.values[hash_code].value


hashtable = Hashtable(1000)
DAYS = 360
stock_history = Hashtable(round(DAYS + DAYS * 0.2))
for path in find_csv_files("data"):
    stock_data = pd.read_csv(path)
    # put every row in the stockhistory hashmap
    for index, day in stock_data.iterrows():
        stock_history.add(day["Date"], day)
    hashtable.add(path[:-4], stock_history)
print(hashtable.search(path[:-4]).search("2022-02-29"))

def is_prime(n):
    for i in range(2, n):
        if n % i == 0:
            return False
    return True

blatt = False
if blatt:
    hashtable = Hashtable(99991)
    print(hashtable.hash_func("FHTechnikumWien"))


