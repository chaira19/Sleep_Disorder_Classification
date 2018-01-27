'''
import sklearn
from sklearn import svm
import random 
from random import shuffle
import numpy as np

file1 = open("iris.data", "r")

temp_counter = 0
pattern_temp = []
pattern = []
correct_class = []

for line in file1.readlines():

    line=line.split(',')
    pattern_temp.append([])  
   
    for i in range(len(line)-1):
        pattern_temp[temp_counter].append(float(line[i]))

    if temp_counter<50:
        #pattern_temp[temp_counter].append(0)
        correct_class.append(0)
    elif temp_counter<100:
        #pattern_temp[temp_counter].append(1)
        correct_class.append(1)
    else:
        #pattern_temp[temp_counter].append(2)
        correct_class.append(2)
    
    temp_counter=temp_counter+1 

c = zip(pattern_temp, correct_class)
random.shuffle(c)
pattern_temp, correct_class = zip(*c)

features_train = np.array(pattern_temp[0:125])
features_test = pattern_temp[126:148]

labels_train = np.array(correct_class[0:125])
labels_test = correct_class[126:148]

#features_train = list(map(int, features_train))
#features_test = list(map(int, features_test))

features_train = np.array([[(float(j)) for j in i] for i in features_train])
features_test = np.array([[(float(j)) for j in i] for i in features_test])
labels_train = np.array(list(map(int, labels_train)))
labels_test = np.array(list(map(int, labels_test)))

print features_train
print labels_train
print len(features_train)
print len(labels_train)
for i in features_train:
    print len(i)
#features_train = np.array(features_train).astype(np.float)
#features_test = np.array(features_test).astype(np.float)
print type(features_train[0])

for i in range(len(labels_train)):
    print features_train[i]
    print " "
    print labels_train[i]
    print "\n"

#from sklearn.ensemble import RandomForestClassifier
from sklearn import svm, tree
clf = svm.SVC()
clf.fit(features_train, labels_train)
pred = clf.predict(features_test)

accuracy = 0
for i in range(labels_test):
    if(labels_test[i] == pred[i]):
        accuracy = accuracy + 1

accuracy = (accuracy/len(labels_test))*100

'''
from sklearn.datasets import load_iris
from random import shuffle
import numpy as np

iris = load_iris()
new_data = zip(iris.data, iris.target)
shuffle(new_data)
training_data = new_data[0:120]
features_train, labels_train = zip(*training_data)
testing_data = new_data[121:149]
features_test, labels_test = zip(*testing_data)

## using default functions of sklearn
def iris_scikit_learn():
    
    from sklearn import tree, svm
    #clf = tree.DecisionTreeClassifier()
    clf = svm.SVC()
    clf = clf.fit(features_train, labels_train)
    pred = clf.predict(features_test)

    accuracy = 0
    for i in range(len(labels_test)):
        if(labels_test[i] == pred[i]):
            print "yes"
            accuracy = accuracy + 1
        else:
            print "no"

    accuracy = float((accuracy*100/len(labels_test)))
    print accuracy
    '''
    print pred
    print labels_test
    print len(pred)
    print len(labels_test)


    print iris.data
    print len(iris.data)
    print iris.target
    print len(iris.target)

    '''
def iris_neural_network():
    training_data = new_data[0:120]
    features_train, labels_train = zip(*training_data)
    testing_data = new_data[121:149]
    features_test, labels_test = zip(*testing_data)
    import network
    net = network.Network([4, 4, 1])
    features_train = [np.reshape(x, (4,1)) for x in features_train]
    training_data = zip(features_train, labels_train)
    features_test = [np.reshape(x, (4,1)) for x in features_test]
    testing_data = zip(features_test, labels_test)
    net.SGD(training_data, 30, 1, 0.0001, test_data = testing_data)

#iris_neural_network()
iris_scikit_learn()