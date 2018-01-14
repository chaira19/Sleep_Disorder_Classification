## library to play with physionet datasets
import wfdb

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
def load_data():
	## Initializing list
	data = []
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

	for d in data:
		print d
	print len(data)

load_data()

'''


for item in annotations1:

	#if item[1][0] is 'D' :
		#continue

	if int(item[2]) < 15000:
		value = []
		#value.append(original_data[int(item[2])+2])
		value.append(int(signals2(int(item(2))+2)[0]))
		value.append(item[7])
		newdata[k] = value
		k = k + 1
'''

