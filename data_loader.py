import wfdb
from IPython.display import display

record1 = wfdb.rdsamp('Sleep_MIT_Dataset/slp01a')

record2 = wfdb.rdsamp('Sleep_MIT_Dataset/slp02b')

display(record2)

signals1, fields1 = wfdb.srdsamp('Sleep_MIT_Dataset/slp01a', sampfrom=1, sampto = record1.siglen)

signals2, fields2 = wfdb.srdsamp('Sleep_MIT_Dataset/slp02b', sampfrom=1, sampto = record2.siglen)
