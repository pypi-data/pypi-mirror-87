from DataProcessing.DataProcessor import DataProcessor

# 5 here means the minimum length of each sentences
dataProcessor = DataProcessor(5)
# X is the [The number of entries * The length of each entry] input list
# Y is the [The number of entries * 1] label list
X, Y = dataProcessor.dataProcessingForRNN("xss-20000.txt", "labeled_data.csv")
X, Y = dataProcessor.dataProcessingForSVM("xss-20000.txt", "labeled_data.csv")
input = "Hello Madam http:fdaoj is good /aspcms/product/2016-12-8/496.html?word=angelina&cl=3&s=angelina&tn=bds&si=www.baidu.com&ct=%22%3E%3Cimg%20src=1%20onerror=alert(1)%3E"
print(dataProcessor.inputProcessingForSVM(input))
print(dataProcessor.inputProcessingForRNN(input))

