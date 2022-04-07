from pydicom import dcmread
from pydicom.data import get_testdata_file
import matplotlib.pyplot as plt
import pydicom
from pydicom.data import get_testdata_files

fpath = get_testdata_file("CT_small.dcm")
ds = dcmread(fpath)

# dal path del file converto in dcm 
fpath2 = 'out/1.3.6.1.4.1.5962.1.1.1.1.1.20040119072730.12322'
with open(fpath2, 'rb') as infile:

    ds = dcmread(infile)


plt.imshow(ds.pixel_array, cmap=plt.cm.bone) 
plt.savefig('images/collo.png')
plt.show()

    
print(ds)
print(ds.SOPClassUID)
print(ds.ImageType)
print(ds.PatientID)
print(ds.PatientSex)
print(ds.pixel_array)



