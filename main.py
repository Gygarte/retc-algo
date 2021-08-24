import requests
import signal

class APIException(Exception):
    pass



# this signal handler allows for a graceful shutdown when CTRL+C is pressed
def signal_handler(signum, frame):
    global shutdown
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    shutdown = True

def main():
    pass



if __name__ == '__main__':
    signal.signal(signal.SIGINT, signal_handler)
    main()
    