import pandas as pd

class Hashtable:

    def __init__(self, size):
        self.size = size
        self.values = [0] * size

    def hash_func(self, key):
        ascii_code = sum([ord(c) for c in key])
        return ascii_code % self.size

    def add(self, key, value):
        hash_code = self.hash_func(key)
        i = 1
        while self.values[hash_code] != 0:
            i = i**2
            hash_code = (hash_code + i) % self.size
            i += 1
        self.values[hash_code] = [key, value]

    def search(self, key):
        hash_code = self.hash_func(key)
        i = 1
        while self.values[hash_code][0] != key:
            i = i ** 2
            hash_code = (hash_code + i) % self.size
            i += 1


        return self.values[hash_code][1]


stock_data = pd.read_csv("MSFT.csv")

hashtable = Hashtable(60)
hashtable.add("MSFT", stock_data)

print(hashtable.search("MSFT"))
