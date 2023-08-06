# -*- coding:utf-8 -*-
import urllib
import re
import nltk
import html
import csv

class NormalDataProcessor(object):
    def __init__(self, min_len):
        self.MIN_LEN = min_len
        self.tokens_pattern = r"RT\s@\w+(:\s)*|&#[0-9]+"
        self.freqdist = {}

    def do_str(self, line):
        return re.sub(self.tokens_pattern, "", line)

    def load_freqdist(self, filename):
        tokens_list = []
        with open(filename, newline='') as f:
            reader = csv.reader(f)
            data = list(reader)
            # print(data[0])
        for i in range(1,len(data)):
            line = data[i][6:][0]
            if len(line) > self.MIN_LEN:
                result = self.do_str(line)
                # print(result)
                tokens_list += re.findall("\w+['\w+]*", result)
        self.freqdist = nltk.FreqDist(tokens_list)
        # print(self.freqdist.keys())
        # print(self.freqdist.values())

    def getFreq(self):
        return self.freqdist

# d = NormalDataProcessor(10)
# d.load_freqdist("labeled_data.csv")