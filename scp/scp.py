from pydicom.uid import ExplicitVRLittleEndian
import os
import time
from pynetdicom import AE, debug_logger, evt, AllStoragePresentationContexts, ALL_TRANSFER_SYNTAXES
from pynetdicom.sop_class import CTImageStorage
from pydicom.filewriter import write_file_meta_info
from pydicom import dcmread
import matplotlib.pyplot as plt
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler


debug_logger()

# def readImg(path):
        # with open(path, 'rb') as infile:
            # ds = dcmread(infile)
            # plt.imshow(ds.pixel_array, cmap=plt.cm.bone) 
            # plt.savefig(f"images{ds.PatientName}-{ds.PatientID}")
            # plt.show()

# -{ds.AcquisitionDateTime}


def handle_store(event, storage_dir):
    """Handle EVT_C_STORE events."""
    # Crea cartella o tira errore 
    try:
        os.makedirs(storage_dir, exist_ok=True)
    except:
        # Unable to create output dir, return failure status
        return 0xC001

    # join del path della cartella con il nome del dataset 
    fname = os.path.join(storage_dir, event.request.AffectedSOPInstanceUID)

    with open(fname, 'wb') as f:
        # Write the preamble, prefix and file meta information elements
        # TODO: Capire bene queste cose
        f.write(b'\x00' * 128)   
        f.write(b'DICM')
        # data_set = dcmread(f)
        write_file_meta_info(f, event.file_meta)
        f.write(event.request.DataSet.getvalue())
        f.save_as()
   
    # readImg(fname)


    return 0x0000


# handlers degli eventi scatenati
handlers = [(evt.EVT_C_STORE, handle_store, ['out'])]

# instanza dell'application entity, entità coinvolta nella comunicazione dicom
ae = AE()

storage_sop_classes = [cx.abstract_syntax for cx in AllStoragePresentationContexts]
for uid in storage_sop_classes:
    ae.add_supported_context(uid, ALL_TRANSFER_SYNTAXES)

ae.add_supported_context(CTImageStorage, ExplicitVRLittleEndian)
ae.start_server(("127.0.0.1", 11112), block=True, evt_handlers=handlers)

