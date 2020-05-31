import cryptocompare
from datetime import datetime

class Currency:

    def __init__(self,name, curr):
        
        self.name = name
        self.curr = curr
        
    def get_price(self):
        return cryptocompare.get_price(self.name,curr = self.curr)[self.name][self.curr]

class Logger:

    def __init__(self, path, step):

        self.path = path
        self.file = open(self.path,'a+')
        self.file.close()
        self.step = step

    def log(self, prices, deltas):
        
        self.file = open(self.path, 'a+')
        self.file.write("%s,%s,%s,%s,%s,%s\n" %( datetime.now(), prices[0], prices[1], deltas[0], deltas[1], self.step))
        self.file.close()

    def get_n_lines(self,n):
        
        self.file = open(self.path,'r')
        lines = self.file.readlines()
        self.file.close()
        if not len(lines) == 0:
            flag = 0
            while not flag:
                try:
                    lines[-n-1:-1]
                    flag = 1
                except:
                    n = n - 1
            return lines[-n-1:-1]
        return None
    
    def get_last_line(self):

        self.file = open(self.path,'r')
        lines = self.file.readlines()
        self.file.close()
        print(lines)
        if not len(lines) == 0:
            return lines[-1]
        return None
