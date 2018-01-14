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

		#if item[1][0] is 'D' :
		#	continue

		if int(item[2]) < int(record.siglen):

			value.append(signals[int(item[2])])
			value.append(item[7])
			data.append(value)

	#return data

data = []

annotation_features('slp01a', "annotations1", data)

for d in data:
	print d

# function to load and add data from text file
#def append_from_text(previous_data, newfile_path)


### original_data = [i.strip().split() for i in open("Dataset_Modified_Form/slp01b.txt").readlines()]

#print annotations
#print original_data





		
	#print item
	#print "\n"




'''annotations1 = [i.strip().split() for i in open("Dataset_Modified_Form/annotations5.txt").readlines()]

#original_data1 = [i.strip().split() for i in open("Dataset_Modified_Form/slp14.txt").readlines()]


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

