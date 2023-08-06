# RandomForest<br />
RandomForest module for detecting xss payload<br />
make sure to install DataProcess in the same project path<br />

#train the mode:
train(X_train,Y_train)<br />

#load the saved model
loadfile()<br />

#detect the user input:
detect_userinput(USER_INPUT_VALUE,rfmodel)<br />
#if return value equals 0, it means this is a XSS attack payload 
#if return value equals 1, it means this is a benign user input