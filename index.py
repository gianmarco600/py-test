from pydicom import dcmread
from pydicom.data import get_testdata_file

fpath = get_testdata_file("CT_small.dcm")
ds = dcmread(fpath)

print(ds)