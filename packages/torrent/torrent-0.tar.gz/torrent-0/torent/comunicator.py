"""python variable scharer

the class implementation of a variable scharer for python
"""
import socket, threading, time
from jpe_types.paralel import LockableThread, threadInharitanceFilter
from jpe_types.conversions.intager import baseN

from torent.client import client
import logging

NoneType = type(None)
"the type of None"

class comunicator:
    """the basic comunicator 

    will be used by more advanced comunicators to comunicate with one another basicly averything that habpens on the server and the client related to socket
    """
    _initiated = False
    def __init__(self, port: int, protocol=socket.AF_INET, sockType=socket.SOCK_STREAM, proto=0, name=None, log=None, bufferSize=2048, initFunc=None):
        """construct the comunicator

        @param port: witch port the sockets are crated with
        @type port: int

        @param protocol: These constants represent the address (and protocol) families, used for the first argument to socket(). If the AF_UNIX constant is not defined then this protocol is unsupported. More constants may be available depending on the system.
        @type protocol: socket.AF_INET, socket.AF_INET6, socket.AF_UNIX, AF_CAN, AF_PACKET, or AF_RDS.

        @param sockType: These constants represent the socket types, used for the second argument to socket(). More constants may be available depending on the system. (Only SOCK_STREAM and SOCK_DGRAM appear to be generally useful.)
        @type sockType:  socket.SOCK_STREAM, socket.SOCK_DGRAM, socket.SOCK_RAW, socket.SOCK_RDM, socket.SOCK_SEQPACKET

        @param proto: The protocol number is usually zero and may be omitted or in the case where the address family is AF_CAN the protocol should be one of CAN_RAW, CAN_BCM, CAN_ISOTP or CAN_J1939.
        @type proto: socket.constant

        @param name: the name of the communicator will be used by other istances to reference this one if None (default) the server will construct a unique one
        @type name: str

        @param log: the logger used to log proceses made by the comunicator
        @type log: loggging.logger

        @param bufferSize: the buffersize for recv data
        @type bufferSize: int

        @param func: the function we want to run with parameter client when a new client is connected, if the return of the
        function is True the client will not be saved, this function is blocking so the connector wont lissen while its running
        @type func: function with 1 parameter
        """

        assert type(port) is int, "port must be an int"
        self.port = port
        """witch port to operate on"""

        assert isinstance(name, (str, NoneType)), "the name must be as string"
        self.name = self._getUUID_for_client(port) if name is None else name
        """the uuid of the instance if None server Generated"""

        self.sockData = protocol, sockType, proto
        "a tuple containing the the sockets protocol and the sockType"

        self.connections = {}
        """a dict containing the socket connections of the comunicator by uuid

        uuid is the unike unit id aka the id used by the name of the connected communicator
        """

        assert isinstance(log, (logging.Logger, type(None))), "logger must be None or a logger"
        self.logger = log
        "the logger used to log activity made this class"

        self.listeningThread=None
        """the thread used for listening
        
        initates to none\n
        to start listening run stert_listen() method
        to resume run setListenActivity(True) and to pause listening run setListenActivity(False)"""

        assert type(bufferSize) is int, f"buffersize must be an int not {type(bufferSize)}"
        self.buffer = bufferSize
        "the buffersize for socket recv"

        self.data = {"torent_getClientInit": (self._torent_getClientInit, {}),
                     "torent_connectToNewConectors": (self._connectToNewConectors, {}),
                     "torent_finischedInput": (self._finischedInput, {}),
                     "torent_unlockClient": (self.unlockClient, {}),
                     "torent_endClientInit": (self._clientComleat, {})}
        """who is data updated

        a dict refrencing torent names and function to update python variables
        """
        self.init_Lock = threading.Lock()
        """initialisation lock
        
        the initalisation lock that is used by holdTilInit to lock threads until initiation is done"""

        self.start_listen(initFunc)
        self._initiated = True
    
    def addDataPoint(self, key, val, **specification):
        """adds a new data point

        adds datapoint with internal name key and value val
        
        @param val: the function to be executed when value is changed this schould set val to whatever u want
        @type val: function

        @param key: the internal name of the val
        @type key: string

        @param specification: a dict containing execution specification\n
                              built in opions are:
                                None at present
        """
        assert type(key) is str, f"the key must be a string not {type(key)}"
        assert type(val) is type(lambda x:None), f"val must be a function not {type(val)}"
        self.data[key] = (val, specification)
    
    def assertInit(self):
        """make sure instance is initated

        make sure we initated the instance
        """
        assert self._initiated, "communicator must be initiated"
    
    def _log_info(self, msg, *args, **kwargs):
        """make an info call to self.logger

        Logs a message with level DEBUG on this logger. The msg is the message format string, and the args are the arguments which are merged into msg using the string formatting operator. (Note that this means that you can use keywords in the format string, together with a single dictionary argument.) No % formatting operation is performed on msg when no args are supplied.

        There are four keyword arguments in kwargs which are inspected: exc_info, stack_info, stacklevel and extra.

        see https://docs.python.org/3/library/logging.html logger.debug for details
        """
        if not self.logger is None:
            self.logger.info(msg)
    
    def _log_warn(self, msg, *args, **kwargs):
        """make an warn  call to self.logger

        Logs a message with level DEBUG on this logger. The msg is the message format string, and the args are the arguments which are merged into msg using the string formatting operator. (Note that this means that you can use keywords in the format string, together with a single dictionary argument.) No % formatting operation is performed on msg when no args are supplied.

        There are four keyword arguments in kwargs which are inspected: exc_info, stack_info, stacklevel and extra.

        see https://docs.python.org/3/library/logging.html logger.debug for details
        """
        if not self.logger is None:
            self.logger.warn(msg)

    def __str__(self):
        "convert to string currently prints its name"
        return str(self.name)
      

    def start_listen(self, func=None):
        """listens for client connections called by the server 

        will run in a Thread listen for connections ad add them to the connection dict

        @param func: the function we want to run with parameter client when a new client is connected, if the return of the
        function is True the client will not be saved, this function is blocking so the connector wont lissen while its running
        @type func: function with 1 parameter

        """
        assert not self._initiated, "dont call this function"
        if func is None: 
            func = lambda x: None
        #crate a listening socket
        ListeningSock = socket.socket(self.sockData[0], self.sockData[1], proto=self.sockData[2])
        # the thing the thread is gona run

        def listen_InThread(*vals: tuple):
            "subscript fore the actual connection"
            self, ListeningSock, port = vals
            self._log_info(f"crated listening Socket {ListeningSock}")
            ListeningSock.bind((socket.gethostname(), port))
            ListeningSock.listen(10)
            while True: 
                self._log_info(f"waiting for clients")
                sock, addres = ListeningSock.accept()
                self._log_info("got client")

                this_client = client(sock, addres, None)
                this_client.name, this_client.ip = this_client.recv(2048)

                this_client.send(self.name)
                self._log_info(f"got client, client name is {this_client.name}")

                if not this_client.name in self.connections and not func(this_client):
                    self.connections[this_client.name] = this_client
                    this_client.startListening(self._updateData, self.buffer)
                    self._log_info("sucessfuly initated the client")

                else: self._log_info("did not crate client")
        
        self.listeningThread = LockableThread(target=listen_InThread, 
                                              args=[self, ListeningSock, self.port], 
                                              name=f"{self.name}_listeningThread",
                                              daemon=True)
        "the thread used to listen for connections"
        self.listeningThread.start()
        self._log_info(f"started listening Thread for communicator {self.name}")
    
    def setListenActivity(self, activity=False):
        """sets the activity of the listening thread

        activates or distactivates the listening Thread
        
        @param activity: if True unlock the thread if false lock it
        @type activity: bool
        """
        if activity:
            self._log_info("activated listening Thread")
            self.listeningThread.releace()
        else: 
            self._log_info("locked listening Thread")
            self.listeningThread.aquire()

    def connect(self, ip, func=None, port=None):
        """connect to a new master

        crate a conection to a comunicator at ip ip and port self.port

        @param ip: the ip addres of the master
        @type ip: string ipadress

        @param func: the function we want to run with parameter client when a new client is connected, if the return of the
        function is True the client will not be saved, this function is blocking so the connector wont lissen while its running
        @type func: function with 1 parameter

        @param port: the port to conect to defaults to the listening port
        @type port: int
        """
        if not type(port) is int:
            port=self.port

        assert type(port) is int, f"the port must be an int plz dont set self.port manulay {type(port)}"

        if func is None: 
            func = lambda x: None

        sock = socket.socket(self.sockData[0], self.sockData[1], proto=self.sockData[2])
        sock.connect((ip, port))
        #crate client
        this_client = client(sock, (ip, port), None)
        self._log_info("crated client")
        # send owne name
        this_client.send((self.name, (socket.gethostbyname(socket.gethostname()), self.port)))
        this_client.name = this_client.recv(2048)
        self._log_info(f"comunicator {self.name} has crated client with name {this_client.name}")
        if not this_client.name in self.connections:
            self.connections[this_client.name] = this_client
            this_client.startListening(self._updateData, self.buffer)
            self._log_info(f"crated newClient")

    def _getUUID_for_client(self, port):
        """generats a uuid for the client

        genrate a uuid form id
        """
        ip = socket.gethostbyname(socket.gethostname())
        uuid = baseN(int(str(port) + "".join([x.zfill(3) for x in ip.split(".")])), 36)
        return uuid

    def send(self, data, clients=None, blackList=[]):
        """send data to all clients

        go throw every client and send data

        @param clients: names of the clients to update if None(defauld) that means all
        @type clients: list

        @param blackList: what clients not to update under any circumstances
        @type blackList: list
        """
        if clients is None:
            clients = self.connections
        
        assert isinstance(blackList, (list, tuple, dict)), f"make blackList a list not  {type(blackList)}"
        
        assert isinstance(blackList, (dict, list, tuple)), f"clients must be list, tuple of dict not {type(clients)}"
        for client in clients:
            assert client in self.connections, "invalid client {client} not in client dict"
            if client in blackList:
                continue
            self.connections[client].send(data)
            self._log_info(f"send data {data} to client {self.connections[client].name}")

    def _updateData(self, key, val, client):
        """run update function

        runs the update function data[key] with args val[0] and kwargs val[1]

        @param key: the torent name of the function to be run
        @type key: string

        @param val: a list containing a tuple at position 0 and a dict at position 1 containing args and kwargs respectivly
        @type val: list, tuple, dict
        """
        assert type(key) is str, f"the key must be a string not {type(key)}"
        assert type(val) in [list, tuple, dict], f"val must be a list, tuple or dict not {type(val)}"
        if type(val) is dict:
            args = val["args"] if "args" in val else ()
            kwargs = val["kwargs"] if "kwargs" in val else {}
        else:
            args = val[0] if len(args) else ()
            kwargs = val[1] if len(args) >=2 else {}

        if key in self.data:
            self._log_info(f"execute function {key} from communicator {self.name} in thread")
            fun, funSpecific = self.data[key]
            assert type(fun) is type(lambda x:None) or type(fun) is type(self._torent_getClientInit), "fun must be a function or method not {type(fun)}"
            t= LockableThread(target=fun,
                             args=(client, *args),
                             kwargs=kwargs,
                             name=f"runFun {key} from torent comunicator {self.name}")
            t.start()
        else:
            self._log_warn(f"function {key} not found in data for comunicator {self.name}")

    def updateVar(self, key, *args, **kwargs):
        """update a value

        run function with torent name key on all possible clients

        note: you may not use clients and blackList as kwargs in your function as they are pased to send
        see send for more details
        
        @param key: the torent name of the function to be executed folowed by the parametrs to be passed
        @type key: string
        """
        if "clients" in kwargs:
            clients = kwargs["clients"]
            del kwargs["clients"]
        else: clients = None

        if "blackList" in kwargs:
            blackList = kwargs["blackList"]
            del kwargs["blackList"]
        else: blackList = []

        self.send(self._encriptData(key, args, kwargs=kwargs), clients=clients, blackList=blackList)
    execute = updateVar

    def _encriptData(self, key, args, kwargs):
        "get data to be serialized"
        data = (key, {"args": args, "kwargs": kwargs})
        return data
    
# init functions
    def postInit(self):
        """updates scharing graph to incoporate this comunicator

        it is not recomended to use this function as unforcean problems may arise
        """
        self.getOtherConections()
        self.holdTilInit()

    def getOtherConections(self):
        """tells server to run functon on this client with all the ips as arguments

        this dose only work if ips are diferent otherwise go wire propergation
        """
        args = []
        for client in self.connections:
            args.append(self.connections[client].name)
        self.updateVar("torent_getClientInit", *tuple(args))
    
    def _torent_getClientInit(self, clientInit, *args):
        """run function with all conected ips as addreses

        run a function containing the values of the ips adresses conected to it except the client and all in args
        """

        ignore = (clientInit.name, *args)
        newVals = []
        for client in self.connections.values():
            if not client.name in ignore:
                newVals.append(client.ip)

        self.updateVar("torent_connectToNewConectors", *tuple(newVals), clients=[clientInit.name])
    
    def _connectToNewConectors(self, client, *args):
        "run by _torent_getClientInit to initate all the clients not contained in this client conection dict"
        for ip in args:
            self._log_info(f"connecting to client with ip {ip}")
            self.connect(ip[0], port=ip[1])
        
        
        self.updateVar("torent_endClientInit", clients=[client.name])
    
    def holdTilInit(self):
        """hold thread unit server has finisched setup

        hold current thread until we finich initation of torent
        """
        self.init_Lock.acquire()
        while self.init_Lock.locked():
            time.sleep(.1)
    
    def unlockClient(self, *args):
        "unclocks the client part of init protocol"
        self._log_info(f"communicator {self.name} is ready to go")
        if self.init_Lock.locked(): self.init_Lock.release()
    
    def _finischedInput(self, *args, **kwargs):
        "unock init hold lock"
        args = []
        for client in self.connections:
            args.append(self.connections[client].name)
        self.updateVar("torent_getClientInit", *tuple(args),)
    
    def finischSetup(self):
        """finalizes setup for graphes
        """
        self._clientsRemainingToInit = len(self.connections)
        self.updateVar("torent_finischedInput")
        self.holdTilInit()
    
    def _clientComleat(self, client):
        """remove 1 from client to be initateded counter
        """
        logging.info(f"client {client.name} has finisched init")
        if hasattr(self, "_clientsRemainingToInit"):
            self._clientsRemainingToInit -= 1
        else: 
            "only if run from postscripter"
            self._clientsRemainingToInit = 0

        if self._clientsRemainingToInit <= 0:
            self.updateVar("torent_unlockClient")
            self.unlockClient()


def decriptUUIDname(uuid):
    """converts a uuid gerated by the system to 

    converts a uuid gerated by the system to ip and port
    @param uuid: the uuid to decript
    @type uui: str
     """
    assert isinstance(uuid, str), f"the uuid must be a string not {type(uuid)}"
    key = str(int(uuid, 36))
    ip = str(int(key[-12:-9])) + "." + str(int(key[-9:-6])) + "."+ str(int(key[-6:-3])) + "." + str(int(key[-3:]))
    return ip, int(key[:-12])