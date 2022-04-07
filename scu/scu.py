from pydicom import dcmread
import time
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler
from pynetdicom import AE, debug_logger
from pynetdicom.sop_class import CTImageStorage

debug_logger()

# Definizione watcher
def watcher():
    if __name__ == "__main__":
        patterns = ["*"]
        ignore_patterns = None
        ignore_directories = False
        case_sensitive = True
        my_event_handler = PatternMatchingEventHandler(patterns, ignore_patterns, ignore_directories, case_sensitive)


    def on_created(event):
       print(f"hey, {event.src_path} has been created!")
       ds = dcmread(event.src_path)
       eventHandler(ds)

    my_event_handler.on_created = on_created

    path = "input"
    observer = Observer()
    observer.schedule(my_event_handler, path)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        observer.join()

# Definizione eventHandler
# def eventHandler(assoc, path): 
#     # Read in our DICOM CT dataset
#     ds = dcmread(path)
def eventHandler(ds):
    # Associate with peer AE at IP 127.0.0.1 and port 11112
    assoc = ae.associate("127.0.0.1", 11112)

    if assoc.is_established:
        # Use the C-STORE service to send the dataset
        # returns the response status as a pydicom Dataset
        status = assoc.send_c_store(ds)

        # Check the status of the storage request
        if status:
                # If the storage request succeeded this will be 0x0000
            print('C-STORE request status: 0x{0:04x}'.format(status.Status))
        else:
            print('Connection timed out, was aborted or received invalid response')

        # Release the association
        assoc.release()
    else:
        print('Association rejected, aborted or never connected')


# Esecuzione servizio
# Initialise the Application Entity
ae = AE()

# Add a requested presentation context
ae.add_requested_context(CTImageStorage)

# Watcher sulla cartella Input
watcher()