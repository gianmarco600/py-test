import time
from pydicom import dcmread
import matplotlib.pyplot as plt
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler

debug_logger()

def watcher():
    patterns = ["*"]
    ignore_patterns = None
    ignore_directories = False
    case_sensitive = True
    my_event_handler = PatternMatchingEventHandler(patterns, ignore_patterns, ignore_directories, case_sensitive)


    print('STO NEL WATCHERRRRRRRRRRRRRRRRRR')

    def on_created(event):
       
        print('STO NEL CREATEEEEE')

        ds = dcmread(event.src_path)
        # print(ds)
        plt.imshow(ds.pixel_array, cmap=plt.cm.bone) 
        plt.savefig(f"out\images\{ds.PatientName}-{ds.PatientID}")


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
