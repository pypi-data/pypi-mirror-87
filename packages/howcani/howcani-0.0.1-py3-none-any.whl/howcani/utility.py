import threading

def run_on_thread(function, *args):
    thread = threading.Thread(target=function, args=args)
    thread.daemon = True
    thread.start()