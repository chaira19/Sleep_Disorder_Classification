## importing modules
import csv
import numpy as np

datContent = [i.strip().split() for i in open("Sleep_MIT_Dataset/slp01a.hea").readlines()]

datanew = [i.strip().split() for i in open("annotations.txt").readlines()]

# write it as a new CSV file
with open("Sleep_MIT_Dataset/slp02a.csv", "wb") as f:
    writer = csv.writer(f)
    writer.writerows(datContent)

data = np.fromfile("Sleep_MIT_Dataset/slp01a.dat")
print data

#print datContent

#print datanew
