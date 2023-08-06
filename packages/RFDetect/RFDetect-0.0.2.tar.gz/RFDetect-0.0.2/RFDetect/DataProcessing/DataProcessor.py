from DataProcessing.MalwareDataProcessor import MalwareDataProcesser
from DataProcessing.NormalDataProcessor import NormalDataProcessor
import urllib
import re
import html
import csv
import random

class DataProcessor(object):
    def __init__(self, min_len):
        self.MIN_LEN = min_len
        self.freqdist = {}
        self.index_wordbag=0
        self.wordbag={}

    def load_freqdist(self, dist1, dist2):
        self.freqdist = {**dist1, **dist2}

    # Load the wordbag from the frequency distribution dictionary. tag the words that repeat less than min times with -1.
    def load_wordbag(self, min):
        keys = list(self.freqdist.keys())
        for localkey in keys:
            if localkey in self.wordbag.keys():
                continue
            elif self.freqdist.get(localkey, 0) <= min:
                self.wordbag[localkey] = -1
            else:
                self.wordbag[localkey] = self.index_wordbag
                self.index_wordbag += 1

    # Reset all the fields back to its initial state.
    def clearAll(self):
        self.freqdist = {}
        self.index_wordbag = 1
        self.wordbag = {}

    def makeAlign(self, entry, length):
        if length > len(entry):
            return entry + [0]*(length - len(entry))
        return entry

    def regularize(self, entries):
        mlen = 0
        for entry in entries:
            mlen = max(mlen, len(entry))
        for i in range(len(entries)):
            entries[i] = self.makeAlign(entries[i], mlen)

    def shaffle(self, entries, labels):
        x = list(range(len(entries)))
        random.shuffle(x)
        entries = [entries[i] for i in x]
        labels = [labels[i] for i in x]
        return entries, labels

    def inputProcessingForSVM(self, input):
        line, number = re.subn(r'\d+', "8", input)
        # ulr replaced to http://u
        line, number = re.subn(r'(http|https)://[a-zA-Z0-9\.@&/#!#\?:=]+', "http://u", line)
        # clear the comments
        line, number = re.subn(r'\/\*.?\*\/', "", line)
        malwareDataProcessor = MalwareDataProcesser(self.MIN_LEN)
        normalDataProcessor = NormalDataProcessor(self.MIN_LEN)
        line = normalDataProcessor.do_str(line)
        line = re.findall("\w+['\w+]*", line)
        temp = ""
        for str in line:
            temp += " "
            temp += str
        words = malwareDataProcessor.do_str(temp)
        vers = [0] * (self.index_wordbag + 1)
        for word in words:
            if word in self.wordbag.keys():
                index = self.wordbag[word]
                vers[index] += 1
            else:
                vers[-1] += 1
        return vers

    def inputProcessingForRNN(self, input):
        line, number = re.subn(r'\d+', "8", input)
        # ulr replaced to http://u
        line, number = re.subn(r'(http|https)://[a-zA-Z0-9\.@&/#!#\?:=]+', "http://u", line)
        # clear the comments
        line, number = re.subn(r'\/\*.?\*\/', "", line)
        malwareDataProcessor = MalwareDataProcesser(self.MIN_LEN)
        normalDataProcessor = NormalDataProcessor(self.MIN_LEN)
        line = normalDataProcessor.do_str(line)
        line = re.findall("\w+['\w+]*", line)
        temp = ""
        for str in line:
            temp += " "
            temp += str
        words = malwareDataProcessor.do_str(temp)
        vers = []
        for word in words:
            if word in self.wordbag.keys():
                vers.append(self.wordbag[word])
            else:
                vers.append(-1)
        return vers


    def dataProcessingForSVM(self, malFile, normFile):
        entries = []
        labels = []
        self.clearAll()
        # Ignore the inputs with length <= min_len.
        malwareDataProcessor = MalwareDataProcesser(self.MIN_LEN)
        # Load the frequency distribution from the training dataset.
        malwareDataProcessor.load_freqdist(malFile)
        # Ignore the inputs with length <= min_len.
        normalDataProcessor = NormalDataProcessor(self.MIN_LEN)
        # Load the frequency distribution from the training dataset.
        normalDataProcessor.load_freqdist(normFile)
        # Merge the two fq sets
        self.load_freqdist(malwareDataProcessor.getFreq(), normalDataProcessor.getFreq())
        # Load wordbag from the fq dictionary. Tag -1 for those words that appear less than 10 times.
        self.load_wordbag(10)
        # Start loading malware data input:
        with open(malFile) as f:
            for line in f:
                line = line.strip('\n')
                # url解码
                line = urllib.parse.unquote(line)

                # 处理html转义字符
                line = html.unescape(line)
                if len(line) >= self.MIN_LEN:
                    # print "Learning xss query param:(%s)" % line
                    # number replaced to 8
                    line, number = re.subn(r'\d+', "8", line)
                    # ulr replaced to http://u
                    line, number = re.subn(r'(http|https)://[a-zA-Z0-9\.@&/#!#\?:=]+', "http://u", line)
                    # clear the comments
                    line, number = re.subn(r'\/\*.?\*\/', "", line)
                    words = malwareDataProcessor.do_str(line)
                    vers = [0]*(self.index_wordbag+1)
                    for word in words:
                        if word in self.wordbag.keys():
                            index = self.wordbag[word]
                            vers[index] += 1
                        else:
                            vers[-1] += 1
                    entries.append(vers)
                    labels.append(0)
        # Start loading normal data input
        with open(normFile, newline='') as f:
            reader = csv.reader(f)
            data = list(reader)
            # print(data[0])
        for i in range(1,len(data)):
            line = data[i][6:][0]
            if len(line) > self.MIN_LEN:
                line = normalDataProcessor.do_str(line)
                words = re.findall("\w+['\w+]*", line)
                vers = [0] * (self.index_wordbag + 1)
                for word in words:
                    if word in self.wordbag.keys():
                        index = self.wordbag[word]
                        vers[index] += 1
                    else:
                        vers[-1] += 1
                entries.append(vers)
                labels.append(1)

        # # The length of each entry.
        # print(len(entries[0]))
        # # The number of entries.
        # print(len(entries))
        # # The number of labels.
        # print(len(labels))
        # Process data
        entries, labels = self.shaffle(entries, labels)
        return entries, labels

    def dataProcessingForRNN(self, malFile, normFile):
        entries = []
        labels = []
        self.clearAll()
        # Ignore the inputs with length <= min_len.
        malwareDataProcessor = MalwareDataProcesser(self.MIN_LEN)
        # Load the frequency distribution from the training dataset.
        malwareDataProcessor.load_freqdist(malFile)
        # Ignore the inputs with length <= min_len.
        normalDataProcessor = NormalDataProcessor(self.MIN_LEN)
        # Load the frequency distribution from the training dataset.
        normalDataProcessor.load_freqdist(normFile)
        # Merge the two fq sets
        self.load_freqdist(malwareDataProcessor.getFreq(), normalDataProcessor.getFreq())
        # Load wordbag from the fq dictionary. Tag -1 for those words that appear less than 10 times.
        self.load_wordbag(10)
        # Start loading malware data input:
        with open(malFile) as f:
            for line in f:
                line = line.strip('\n')
                # url解码
                line = urllib.parse.unquote(line)

                # 处理html转义字符
                line = html.unescape(line)
                if len(line) >= self.MIN_LEN:
                    # print "Learning xss query param:(%s)" % line
                    # number replaced to 8
                    line, number = re.subn(r'\d+', "8", line)
                    # ulr replaced to http://u
                    line, number = re.subn(r'(http|https)://[a-zA-Z0-9\.@&/#!#\?:=]+', "http://u", line)
                    # clear the comments
                    line, number = re.subn(r'\/\*.?\*\/', "", line)
                    words = malwareDataProcessor.do_str(line)
                    vers = []
                    for word in words:
                        if word in self.wordbag.keys():
                            vers.append(self.wordbag[word])
                        else:
                            vers.append(-1)
                    entries.append(vers)
                    labels.append(0)
        # Start loading normal data input
        with open(normFile, newline='') as f:
            reader = csv.reader(f)
            data = list(reader)
            # print(data[0])
        for i in range(1,len(data)):
            line = data[i][6:][0]
            if len(line) > self.MIN_LEN:
                line = normalDataProcessor.do_str(line)
                words = re.findall("\w+['\w+]*", line)
                vers = []
                for word in words:
                    if word in self.wordbag.keys():
                        vers.append(self.wordbag[word])
                    else:
                        vers.append(-1)
                entries.append(vers)
                labels.append(1)
        # Process data
        self.regularize(entries)
        entries, labels = self.shaffle(entries, labels)
        return entries, labels





