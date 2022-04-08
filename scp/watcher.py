from this import d
from threading import Timer
import time
from pydicom import dcmread, read_file, uid
import matplotlib.pyplot as plt
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler
import os


def watcher():
    patterns = ["*"]
    ignore_patterns = None
    ignore_directories = False
    case_sensitive = True
    my_event_handler = PatternMatchingEventHandler(patterns, ignore_patterns, ignore_directories, case_sensitive)


    print('STO NEL WATCHERRRRRRRRRRRRRRRRRR')

    def on_created(event):
        
        print('STO NEL CREATEEEEE')
        # with open(event.src_path, 'rb') as file:
        ds = dcmread(event.src_path, force=True)
        ds.file_meta.TransferSyntaxUID = uid.ImplicitVRLittleEndian
        print(ds)
        print(type(ds))
        # if ds.PatientName:
        #     name = ds.PatientName
        #     print(name)

        if(len(ds.pixel_array) > 0):
            image= ds.pixel_array
            print(image)
            plt.imshow(image, cmap=plt.cm.bone) 
            plt.savefig(f"out\images\{ds.PatientName}-{ds.PatientID}")
            
        # print(ds)
        # name = ds.PatientName
        # id = ds.PatientID
        
            # os.makedirs(id, exist_ok=True)
            # ds.save_as(f'images\{name}')
            # print(ds.PatientName)
            # print(ds.PatientID)
            # plt.imshow(ds.pixel_array, cmap=plt.cm.bone) 
            # plt.savefig(f"out\images\{ds.PatientName}-{ds.PatientID}")


    my_event_handler.on_created = on_created

    path = "out"
    observer = Observer()
    observer.schedule(my_event_handler, path)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        observer.join()




watcher()
