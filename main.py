import pandas as pd

class Hashtable():

    def __int__(self, size):
        self.size = size
        self.values = [0] * size

    def hash_func(self, stock_code):
        ascii_code = sum([ord(c) for c in stock_code])
        return ascii_code % self.size

    def import_data(self, stock_code, data):
        hash_code = self.hash_func(stock_code)
        if self.values[hash_code] == 0:
            pass

pd.read_csv("MSFT.csv")
hashtable = Hashtable(3)
