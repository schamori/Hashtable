import pandas as pd
import os
import matplotlib.pyplot as plt
import json

DAYS = 30

def find_csv_files(relative_path):
    csv_files = []
    for file in os.listdir(relative_path):
        if file.endswith(".csv"):
            csv_files.append(os.path.join(relative_path, file))
    return csv_files

class MyException(Exception):
    pass

class Entry:
    def __init__(self, key, value, hashcode):
        self.key = key
        self.value = value
        self.hashcode = hashcode

    def __repr__(self):
        return f"{self.key}: {self.value}\n\n\n"

class HashtableEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, list):
            entries = []
            for entry in obj:
                if isinstance(entry, Entry):
                    value = entry.value
                    if isinstance(value, pd.Series):
                        value = value.to_dict()
                    if value:  # only add entries with a value
                        entries.append({'key': entry.key, 'index': entry.hashcode, 'value': value})
            return entries
        elif isinstance(obj, Hashtable):
            return self.default(obj.entries)
        return obj

class HashtableDecoder(json.JSONDecoder):
    def __init__(self, *args, **kwargs):
        json.JSONDecoder.__init__(self, object_hook=self.dict_to_object, *args, **kwargs)

    def dict_to_object(self, d):
        if 'key' in d and 'index' in d and 'value' in d:
            value = d['value']
            if isinstance(value, dict):
                value = pd.Series(value)
            return Entry(d['key'], value, d['index'])
        return d


class Hashtable:

    def __init__(self, size):
        """"Constructor for Hashtable class, initializes size and entries array"""
        self.size = size
        self.entries = [0] * size

    def hash_func(self, key):
        """"Computes the hash code for given key """
        p = 31
        ascii_code = sum([(p ** i) * ord(c) for i, c in enumerate(key)])
        return ascii_code % self.size

    # Adds a new key-value pair to the hashtable
    def add(self, key, value):
        """"Adds a new key-value pair to the hashtable. Uses quadratic Collision"""
        hash_code = self.hash_func(key)
        i = 1
        allowed_tries = self.size * 15
        print(allowed_tries)
        while isinstance(self.entries[hash_code], Entry):
            allowed_tries -= 1
            if allowed_tries == 0:
                raise MyException("This Hashmap is full")
            if self.entries[hash_code] == key:
                raise MyException("This key already exits")
            i = i ** 2
            hash_code = (hash_code + i) % self.size
        self.entries[hash_code] = Entry(key, value, hash_code)

    def get_hashcode(self, key):
        """Returns hashcode of given key"""
        hash_code = self.hash_func(key)
        i = 1
        if self.entries[hash_code] == 0:
            raise KeyError
        while self.entries[hash_code].key != key:
            i = i ** 2
            hash_code = (hash_code + i) % self.size
            if self.entries[hash_code] == 0:
                raise KeyError
            i += 1
        return hash_code

    def search(self, key):
        """Searches for the value associated with the given key in hashtable"""
        return self.entries[self.get_hashcode(key)].value

    def update(self, key, value=0):
        """Updates the value associated with the given key in hashtable"""
        self.entries[self.get_hashcode(key)].value = value

    def delete(self, key):
        """Deletes the key-value pair associated with the given key in hashtable"""
        self.entries[self.get_hashcode(key)] = 0

    def plot(self, key):
        """Plots the stock price graph for given key using matplotlib"""
        graph = self.entries[self.get_hashcode(key)].value
        y = [day.value["Close"] for day in graph.entries if isinstance(day, Entry)]
        plt.plot(range(len(y)), y, label=key)
        plt.xlabel('Days ')
        plt.ylabel('Price ')
        plt.show()

    def save(self, filename):
        """Saves the hashtable to a JSON file"""
        with open(filename, 'w') as outfile:
            json.dump(hashtable, outfile, cls=HashtableEncoder, indent=4)

    def load(self, filename=None, list_=None, create_inner_hashmap=False):
        """Loads the hashtable from a JSON file or list. If create_inter_hashmap is true it will create another hashmap for
        the Entries given. Note that the every entry needs to have a list of entry inside it if this is set to true."""
        if filename is None and list_ is None:
            raise MyException("No path or list given")
        if filename is not None:
            with open(filename, 'r') as infile:
                data = json.load(infile, cls=HashtableDecoder)
        else:
            data = list_
        for entry in data:
            if create_inner_hashmap:
                if not all(isinstance(inner_entry, Entry) for inner_entry in entry.value):
                    raise MyException("You have speficied create_inner_hashmap but your given list or file does not have inner_entries!")
                stock_history = Hashtable(round(DAYS + DAYS * 0.2))
                stock_history.load(list_=entry.value)
                entry.value = stock_history
                self.entries[entry.hashcode] = entry
            else:
                self.entries[entry.hashcode] = entry

    # Clears all key-value pairs from the hashtable
    def clear(self):
        self.entries = [0] * self.size
    def __str__(self):
        return "".join([f"{entry}" for entry in self.entries if isinstance(entry, Entry)])


hashtable = Hashtable(1000)
for path in find_csv_files("data"):
    stock_history = Hashtable(round(DAYS + DAYS * 0.2))
    stock_data = pd.read_csv(path)
    # put every row in the stockhistory hashmap
    for index, day in stock_data.iterrows():
        stock_history.add(day["Date"], day)
    hashtable.add(path[:-4], stock_history)

hashtable.save('hashmap.json')
#hashtable.search("data\\MSFT").save('hashmap.json')

print(hashtable.entries)
hashtable.clear()
hashtable.load(filename='hashmap.json', create_inner_hashmap= True)
print("NACH DEM ERNEUTEN LADEN")
print(hashtable.entries)
hashtable.plot(path[:-4])
