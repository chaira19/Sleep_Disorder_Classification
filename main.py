## library to play with physionet datasets
import wfdb
from random import shuffle
from sklearn import tree, svm, neural_network
from sklearn.neural_network import MLPClassifier

## Function to extract features from data file and labels from annotaion file and link them.
## File name inputs are without formats.
## Function appends lists containg features and labels(as last feature) to the input list.
def annotation_features(Data_Filename, Annotation_Filename, data = []):

	record = wfdb.rdsamp('Sleep_MIT_Dataset/slp01a')                                                
	signals, fields = wfdb.srdsamp('Sleep_MIT_Dataset/slp01a', sampfrom=1, sampto = record.siglen)
	annotations = [i.strip().split() for i in open("Dataset_Modified_Form/" + Annotation_Filename + ".txt").readlines()]

	for item in annotations:
		value = []

		if annotations.index(item) == 0 :
			continue

		if int(item[2]) < int(record.siglen):

			value.append(signals[int(item[2])])
			value.append(item[7])
			data.append(value)

## Function to load the dataset as list of lists
def load_data(data = []):

	## Appending all features and labels in the list
	annotation_features('slp01a', "annotations1", data)
	#annotation_features('slp01b', "annotations2", data)
	annotation_features('slp02a', "annotations3", data)
	annotation_features('slp02b', "annotations4", data)
	annotation_features('slp3', "annotations5", data)
	annotation_features('slp4', "annotations6", data)
	annotation_features('slp14', "annotations7", data)
	annotation_features('slp16', "annotations8", data)
	annotation_features('slp32', "annotations9", data)
	annotation_features('slp37', "annotations10", data)
	annotation_features('slp41', "annotations11", data)
	annotation_features('slp45', "annotations12", data)
	annotation_features('slp48', "annotations13", data)
	annotation_features('slp59', "annotations14", data)
	annotation_features('slp60', "annotations15", data)
	annotation_features('slp61', "annotations16", data)
	annotation_features('slp66', "annotations17", data)
	#annotation_features('slp67x', "annotations18", data)


## Initializing list
data = []
load_data(data)
shuffle(data)
training_data = data[0:3000]
testing_data = data[3001:3777]
features_train, labels_train = zip(*training_data)
features_test, labels_test = zip(*testing_data)
#print features_test, labels_test
#clf = svm.SVC()
clf = MLPClassifier()
#clf = tree.DecisionTreeClassifier()
clf = clf.fit(features_train, labels_train)
pred = clf.predict(features_test)
print pred

accuracy = 0
for i in range(len(labels_test)):
	if(labels_test[i] == pred[i]):
		accuracy = accuracy + 1

accuracy = float((accuracy*100/len(labels_test)))
print accuracy
print len(data)
'''for d in data:
	print d
	'''
'''
import network
import numpy as np
import string

def RepresentsInt(s):
    try: 
        int(s)
        return True
    except ValueError:
        return False

def vectorized_result(j):
    
    e = np.zeros((5, 1))
    if j == 'W':
    	e[0] = 1
    elif RepresentsInt(j):
    	e[j] = 1.0
	return e

data = []
load_data(data)
shuffle(data)
training_data = data[0:3000]
features_train, labels_train = zip(*training_data)
testing_data = data[3001:3777]
features_test, labels_test = zip(*testing_data)
#print labels_train

def sleep_neural_network(features_train, features_test, labels_train, labels_test):
	
	net = network.Network([4, 4, 5])
	features_train = [np.reshape(x, (4,1)) for x in features_train]
	training_results = [vectorized_result(y) for y in labels_train]
	training_data = zip(features_train, training_results)
	features_test = [np.reshape(x, (4,1)) for x in features_test]
	testing_results = [vectorized_result(y) for y in labels_test]
	testing_data = zip(features_test, testing_results)
	net.SGD(training_data, 30, 1, 0.0001, test_data = testing_data)


sleep_neural_network(features_train, features_test, labels_train, labels_test)
'''
