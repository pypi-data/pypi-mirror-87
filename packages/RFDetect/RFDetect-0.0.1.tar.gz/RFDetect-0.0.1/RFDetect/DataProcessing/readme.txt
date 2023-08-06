An example to use dataProcessor:

from DataProcessing.DataProcessor import DataProcessor
# 5 here means the minimum length of each sentences
dataProcessor = DataProcessor(5)
# X is the [The number of entries * The length of each entry] input list
# Y is the [The number of entries * 1] label list
X, Y = dataProcessor.dataProcessingForRNN("xss-20000.txt", "labeled_data.csv") #For RNN
X, Y = dataProcessor.dataProcessingForSVM("xss-20000.txt", "labeled_data.csv") #For SVM

# After loading the wordbag, we can process an input sentence into a word vector:
input = "Hello Good Morning"
wordvec1 = dataProcessor.inputProcessingForSVM(input)
wordvec2 = dataProcessor.inputProcessingForRNN(input)