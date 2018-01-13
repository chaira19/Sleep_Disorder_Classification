import wfdb

#data = {}

# function to load and add data from text file
#def append_from_text(previous_data, newfile_path)

annotations = [i.strip().split() for i in open("Dataset_Modified_Form/annotations1.txt").readlines()]

### original_data = [i.strip().split() for i in open("Dataset_Modified_Form/slp01b.txt").readlines()]

#print annotations
#print original_data

record1 = wfdb.rdsamp('Sleep_MIT_Dataset/slp01a')

record2 = wfdb.rdsamp('Sleep_MIT_Dataset/slp02b')

signals1, fields1 = wfdb.srdsamp('Sleep_MIT_Dataset/slp01a', sampfrom=1, sampto = record1.siglen)

signals2, fields2 = wfdb.srdsamp('Sleep_MIT_Dataset/slp02b', sampfrom=1, sampto = record2.siglen)

newdata = {}

k = 0


for item in annotations:

	value = []

	#if item[1][0] is 'D' :
	#	continue

	if int(item[2]) < 1800000:
		
		#value.append(original_data[int(item[2])+2])
		value.append(signals1[int(item[2])+2])
		#value.append(signals1)
		value.append(item[7])
		newdata[k] = value
		k = k + 1
		
	#print item
	#print "\n"




annotations1 = [i.strip().split() for i in open("Dataset_Modified_Form/annotations5.txt").readlines()]

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

for item in newdata:
	print item, newdata[item]
	print "\n"
