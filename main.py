import pandas as pd
from os import listdir
import random
def find_csv_filenames( path_to_dir, suffix=".csv" ):
    filenames = listdir(path_to_dir)
    return [ filename for filename in filenames if filename.endswith( suffix ) ]
class Hashtable:

    def __init__(self, size):
        self.size = size
        self.values = [0] * size

    def hash_func(self, key):
        ascii_code = sum([ord(c) for c in key]) * random.randint(0,20) # So to values are differnt for similar dates
        return ascii_code % self.size

    def add(self, value, key=None):
        # if the key is not given it will be the Date
        if key is None:
            key = value["Date"]
        hash_code = self.hash_func(key)
        i = 1
        print(key)
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


hashtable = Hashtable(1000)
DAYS = 1000
stock_history = Hashtable(round(DAYS + DAYS * 0.2))
for path in find_csv_filenames(r"C:\Users\morit\Documents\MEGAsync\2 Semester\Algos\data"):
    stock_data = pd.read_csv(f"data/{path}")
    # put every row in the stockhistory hashmap
    stock_data.apply(stock_history.add, axis=1)
    hashtable.add(stock_history, path[:-4])

    print(hashtable.search(path[:-4]))
