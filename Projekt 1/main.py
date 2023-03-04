import pandas as pd
import os
import matplotlib.pyplot as plt



def find_csv_files(relative_path):
    csv_files = []
    for file in os.listdir(relative_path):
        if file.endswith(".csv"):
            csv_files.append(os.path.join(relative_path, file))
    return csv_files

class MyException(Exception):
    pass

class Entry:
    def __init__(self, key, value):
        self.key = key
        self.value = value


class Hashtable:

    def __init__(self, size):
        self.size = size
        self.entries = [0] * size

    def hash_func(self, key):
        p = 31
        ascii_code = sum([(p ** i) * ord(c) for i, c in enumerate(key)])
        return ascii_code % self.size

    def add(self, key, value):
        hash_code = self.hash_func(key)
        i = 1
        while isinstance(self.entries[hash_code], Entry):
            if self.entries[hash_code] == key:
                raise MyException("This key already exits")
            i = i**2
            hash_code = (hash_code + i) % self.size
            i += 1
        self.entries[hash_code] = Entry(key, value)

    def get_hashcode(self, key):
        hash_code = self.hash_func(key)
        i = 1
        while self.entries[hash_code].key != key:
            i = i ** 2
            hash_code = (hash_code + i) % self.size
            if self.entries[hash_code] == 0:
                raise KeyError
            i += 1
        return hash_code

    def search(self, key):
        return self.entries[self.get_hashcode(key)].value

    def update(self, key, value = 0):
        self.entries[self.get_hashcode(key)].value = value

    def delete(self, key):
        self.entries[self.get_hashcode(key)] = 0

    def plot(self, key):
        graph = self.entries[self.get_hashcode(key)].value
        y = [day.value["Close"] for day in graph.entries if isinstance(day, Entry)]
        plt.plot(range(len(y)), y, label=key)
        plt.xlabel('Days ')
        plt.ylabel('Price ')

        plt.show()

    def __str__(self):
        return "\n\n".join([ f"{entry.key}: {entry.value}\n" for entry in self.entries if isinstance(entry, Entry)])



hashtable = Hashtable(1000)
DAYS = 360
stock_history = Hashtable(round(DAYS + DAYS * 0.2))
for path in find_csv_files("data"):
    stock_data = pd.read_csv(path)
    # put every row in the stockhistory hashmap
    for index, day in stock_data.iterrows():
        stock_history.add(day["Date"], day)
    hashtable.add(path[:-4], stock_history)

    
hashtable.plot(path[:-4])
def is_prime(n):
    for i in range(2, n):
        if n % i == 0:
            return False
    return True

blatt = False
if blatt:
    hashtable = Hashtable(99991)
    print(hashtable.hash_func("FHTechnikumWien"))


