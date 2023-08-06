import os
from sklearn.ensemble import RandomForestClassifier
import pickle
from sklearn.model_selection import train_test_split
from DataProcessing.DataProcessor import DataProcessor
# 5 here means the minimum length of each sentences
current_path = os.path.abspath(__file__)
father_path = os.path.abspath(os.path.dirname(current_path) + os.path.sep + ".")
dataProcessor = DataProcessor(5)
X, Y = dataProcessor.dataProcessingForSVM(father_path + "/DataProcessing/xss-20000.txt", father_path + "/DataProcessing/labeled_data.csv")
#X, Y = dataProcessor.dataProcessingForRF("./DataProcessing/xss-20000.txt", "./DataProcessing/labeled_data.csv") #For SVM

X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2, random_state=0)

#train the machine learning model
def train(X_train,Y_train):
    rfmodel = RandomForestClassifier(n_estimators = 10, random_state=30)
    rfmodel.fit(X_train,Y_train)
    #prediction_test = rfmodel.predict(X_test)
    #return rfmodel
    current_path = os.path.abspath(__file__)
    father_path = os.path.abspath(os.path.dirname(current_path) + os.path.sep + ".")
    with open(father_path + "/rfmodel-xss.pkl",'wb') as f:
        pickle.dump(rfmodel,f)
        
#detect userinput using the pre-trained model
def detect_userinput(user_input,rfmodel):
    #create vector of input
    #dataProcessor = DataProcessor(5)
    #X, Y = dataProcessor.dataProcessingForSVM(father_path+"/DataProcessing/xss-20000.txt", father_path + "/DataProcessing/labeled_data.csv")
    #X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.3, random_state=20)
    wordvec = dataProcessor.inputProcessingForSVM(user_input)
    #print(wordvec)
    result = rfmodel.predict([wordvec])
    print(result)
    return result    

#load the pre-trained model to detect user input
def loadmodel():
        current_path = os.path.abspath(__file__)
        father_path = os.path.abspath(os.path.dirname(current_path) + os.path.sep + ".")
        with open(father_path + "/rfmodel-xss.pkl",'rb') as f:
            rfmodel = pickle.load(f)
        return rfmodel


#detect the user input; value 0 indicates this is a XSS threat, otherwise it's not XSS.
if __name__ == '__main__':
    #train(X_train,Y_train)
    rfmodel = loadmodel()
    #detect_userinput("<script> alert(1) </script>",rfmodel)
    detect_userinput("/0_1/include/dialog/config.php?adminDirHand=%22/%3E%3C/script%3E%3Cscript%3Ealert(1);%3C/script%3E",rfmodel)
    #detect_userinput("simple test",rfmodel)
    #detect_userinput("hello world this is a normal input",rfmodel)
    #detect_input("this is a normal input 234556")
