from queue import Queue

HOST = "127.0.0.1"
PORT = 12345
MAX_BIND_RETRIES = 5
INVALID_CHAR_IN_COMMAND = [
    ";",
    "-",
    "!",
    "*",
    "#",
    "?",
    ">",
    "<",
    "/",
    "^",
]


# total number of threads to handle two tasks - accept new connections, 
# - communicate with existing connections 
NUMBER_OF_THREADS = 2 

# 1st thread accepts new connection, 2nd thread communicates with existing connections 
JOB_NUMBER = [1, 2]

# all socket connection objects 
ALL_CONNECTIONS = []

# all socket addresses 
ALL_ADDRESSES = []

# queue 
Q = Queue()
