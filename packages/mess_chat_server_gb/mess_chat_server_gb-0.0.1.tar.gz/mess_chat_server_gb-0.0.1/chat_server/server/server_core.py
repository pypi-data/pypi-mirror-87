"""
The module contains a class and methods describing the network communication
between the server and clients.
"""

import hmac
import os
import select
import sys
import socket
import json
import threading
import time
import logging
import inspect
import functools
import binascii

BASEDIR = os.getcwd()
sys.path.append(BASEDIR)

from common.log import server_log_config
from common.utils import ValidPort, ServerChecker
from common.config import system, methods, codes


class Log_class:
    """
    A logger decorator like a class
    """

    def __init__(self):
        module = os.path.split(sys.argv[0])[-1]

        if module == 'client_main.py':
            self.logger = logging.getLogger('client')
        elif module == 'server_core.py':
            self.logger = logging.getLogger('server')

    def __call__(self, func):
        @functools.wraps(func)
        def log_saver(*args, **kwargs):
            result = func(*args, **kwargs)
            self.logger.debug(
                f'A function/method "{func.__name__}" was called with args "{args[1:]}, {kwargs}.\n'
                f'Callstack: {func.__module__} -> {inspect.stack()[1][3]}')
            return result

        return log_saver


class ChatServerCore(threading.Thread, metaclass=ServerChecker):
    """
    A JIM server network communication class
    """

    port = ValidPort()

    def __init__(self, address, port, database, crypt) -> None:
        self._logger = logging.getLogger('server')

        self.db = database
        self.address = address
        self.port = int(port)
        self.crypt = crypt
        self._clients = []
        self._address_book = {}
        self._responses = {}
        self._auth = {}
        self._session_crypts = {}
        self._get_sys_args()
        self.transport = None
        self._create_transport()

        super().__init__()

    def _get_sys_args(self) -> None:
        """
        Getting arguments if exists.

        :return: None
        """
        try:
            if '-a' in sys.argv:
                self.address = sys.argv[sys.argv.index('-a') + 1]

            if '-p' in sys.argv:
                self.port = int(sys.argv[sys.argv.index('-p') + 1])

        except IndexError:
            self._logger.critical(f'The arguments must be set. Exiting. Args: {sys.argv}')
            sys.exit(1)

    def _create_transport(self) -> None:
        """
        Create a new network transport.

        :return: None
        """
        self.transport = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.transport.bind((self.address, self.port))
        self.transport.settimeout(system.TIMEOUT)
        self.transport.listen(system.MAX_CONNECTIONS)
        self._logger.info(
            f'The Chat server started. '
            f'Address: "{self.address}", '
            f'Port: "{self.port}", '
            f'Maximum available connections: "{system.MAX_CONNECTIONS}".'
        )

    @staticmethod
    def _check_message_fields(message: dict, fields: tuple) -> bool:
        """
        Checking for required fields in a message.

        :param message: A message from a client
        :param fields: A tuple of fields
        :return: True if all of the fields are exists, else False.
        """
        for field in fields:
            if field not in message.keys():
                return False
        return True

    def presence_process(self, request: dict, sock) -> None:
        """
        A presents message handler.
         A presence message example:
         {
            "action": "presence",
            "time": <unix timestamp>,
            "type": "status",
            "user": {
                "username": "C0deMaver1ck",
                "status": "Yep, I am here!"
            }
         }

        :param request: A message from a client.
        :param sock: IP socket
        :return: None
        """
        if self._check_message_fields(request, ("type", "user")):
            username = request.get('user').get("username")
            if username not in self._address_book.keys():
                self._address_book[username] = sock
                self.db.user_login(
                    username=username,
                    ip=sock[0],
                    port=sock[1]
                )
            response = {
                "response_code": codes.c200_OK,
                "time": int(time.time()),
                "message": "OK"
            }

        else:
            response = {
                "response_code": codes.c400_WRONG_REQUEST,
                "time": int(time.time()),
                "message": "Wrong message's fields"
            }

        self._logger.debug(f'Response presence: "{response}"')
        self._responses[sock] = response

    def message_process(self, request: dict, sock) -> None:
        """
        A text message handler.
         A message example:
         {
            "action": "msg",
            "time": <unix timestamp>,
            "to": "username", / "to": "#room_name",
            "from": "username",
            "encoding": "ascii",
            "message": "message"
         }

        :param request: A message from a client
        :param sock: IP socket
        :return: None
        """
        if self._check_message_fields(request, ("to", "from", "message")):
            recipient = request.get("to")
            if recipient in self._address_book.keys():
                self._logger.debug(f'Recipient: "{recipient}" found.')
                sender = request.get("from")
                self.db.inc_message_counter(sender=sender, recipient=recipient)

                # Messages recrypting
                message = self._session_crypts.get(sender).decrypt(request.get("message"))
                message = self._session_crypts.get(recipient).encrypt(message)
                request.update({"message": message})

                self._responses[self._address_book.get(recipient)] = request
                response = {
                    "response_code": codes.c200_OK,
                    "time": int(time.time()),
                    "message": "OK"
                }
            else:
                self._logger.warning(f'Recipient: "{recipient}" not found.')
                response = {
                    "response_code": codes.c400_WRONG_REQUEST,
                    "time": int(time.time()),
                    "message": "Recipient not found"
                }
                self._responses[sock] = response
                self._logger.debug(f'Response: "{response}"')
        else:
            self._logger.warning(f'Wrong messages fields from {sock.getpeername()}')
            response = {
                "response_code": codes.c400_WRONG_REQUEST,
                "time": int(time.time()),
                "message": "Wrong message's fields"
            }

        self._logger.debug(f'Response message: "{response}"')
        self._responses[sock] = response

    def authenticate_1_process(self, request: dict, sock) -> None:
        """
        A  authenticate message of stage 1 handler.
         Message example:
         {
                "action": "authenticate_1",
                "time": <unix timestamp>,
                "username":  "C0deMaver1ck",
         }

        :param request: A message from a client
        :param sock: IP socket
        :return: None
        """
        if self._check_message_fields(request, ("username",)):
            username = request.get("username")
            if username in self._address_book.keys():
                return

            self._address_book[username] = sock

            if self.db.is_exist_user(username=username):
                random_str = binascii.hexlify(os.urandom(64))
                passwd_hash = self.db.get_passwd_hash(username=username)
                hash_ = hmac.new(passwd_hash, random_str, 'MD5')
                self._auth[username] = hash_
                response = {
                    "response_code": codes.c511_NETWORK_AUTHENTICATION_REQUIRED,
                    "time": int(time.time()),
                    "message": random_str.decode('ascii')
                }
            else:
                response = {
                    "response_code": codes.c404_NOT_FOUND,
                    "time": int(time.time()),
                    "message": "User not found!"
                }
        else:
            response = {
                "response_code": codes.c400_WRONG_REQUEST,
                "time": int(time.time()),
                "message": "Wrong message's fields"
            }

        self._logger.info(f'Response authenticate_1: "{response}"')
        self._responses[sock] = response

    def authenticate_2_process(self, request: dict, sock) -> None:
        """
        A  authenticate message of stage 2 handler.
         Message example:
         {
                "action": "authenticate_2",
                "time": <unix timestamp>,
                "username":  "C0deMaver1ck",
                "message" <digest>
         }

        :param request: A message from a client.
        :param sock: IP socket
        :return: None
        """
        if self._check_message_fields(request, ("username", "message")):
            username = request.get("username")
            client_digest = binascii.a2b_base64(request.get("message"))

            hash_ = self._auth.pop(username)
            digest = hash_.digest()

            if hmac.compare_digest(digest, client_digest):
                self.db.user_login(
                    username=username,
                    ip=sock.getpeername()[0],
                    port=sock.getpeername()[1]
                )
                response = {
                    "response_code": codes.c202_ACCEPTED,
                    "time": int(time.time()),
                    "message": "Accepted"
                }
                self._session_crypts[username] = self.crypt(key_string=(digest * 2))
            else:
                response = {
                    "response_code": codes.c401_UNAUTHORIZED,
                    "time": int(time.time()),
                    "message": "Unauthorized"
                }
        else:
            response = {
                "response_code": codes.c400_WRONG_REQUEST,
                "time": int(time.time()),
                "message": "Wrong message's fields"
            }

        self._logger.debug(f'Response authenticate_2: "{response}"')
        self._responses[sock] = response

    def quit_process(self, request: dict, sock) -> None:
        """
        A quit message handler.
         Message example:
         {
                "action": "quit",
                "time": <unix timestamp>,
                "username":  "C0deMaver1ck",
         }

        :param request: A message from a client.
        :param sock: IP socket
        :return: None
        """
        if self._check_message_fields(request, ("username",)):
            username = request.get("username")
            self.db.user_logout(username=username)
            self._address_book.pop(username)

        else:
            response = {
                "response_code": codes.c400_WRONG_REQUEST,
                "time": int(time.time()),
                "message": "Wrong message's fields"
            }

        self._logger.debug(f'Response quit: "{response}"')
        self._responses[sock] = response

    def get_contacts_process(self, request: dict, sock) -> None:
        """
        An get contacts message handler.
         Message example:
         {
            "action": "get_contacts",
            "time": <unix timestamp>,
            "username": "username"
         }

        :param request: A message from a client.
        :param sock: IP socket
        :return: None
        """
        if self._check_message_fields(request, ("username",)):
            username = request.get("username")
            contacts = self.db.get_user_contacts(username=username)
            response = {
                "response_code": codes.c202_ACCEPTED,
                "time": int(time.time()),
                "message": contacts
            }
        else:
            response = {
                "response_code": codes.c400_WRONG_REQUEST,
                "time": int(time.time()),
                "message": "Wrong message's fields"
            }

        self._logger.debug(f'Response get_contacts: "{response}"')
        self._responses[sock] = response

    def add_contacts_process(self, request: dict, sock) -> None:
        """
        An add contacts message handler.
         Message example:
         {
            "action": "add_contact",
            "time": <unix timestamp>,
            "username": "username"
            "contact": "username"
         }

        :param request: A message from a client
        :param sock: IP socket
        :return: None
        """
        if self._check_message_fields(request, ("username", "contact")):
            username = request.get("username")
            contact = request.get("contact")
            self.db.add_user_contact(user=username, contact=contact)
            response = {
                "response_code": codes.c201_CREATED,
                "time": int(time.time()),
            }
        else:
            response = {
                "response_code": codes.c400_WRONG_REQUEST,
                "time": int(time.time()),
                "message": "Wrong message's fields"
            }

        self._logger.debug(f'Response add_contacts: "{response}"')
        self._responses[sock] = response

    def del_contacts_process(self, request: dict, sock) -> None:
        """
        A deleting contacts message handler.
         Message example:
         {
            "action": "del_contact",
            "time": <unix timestamp>,
            "username": "username"
            "contact": "username"
         }

        :param request: A message from a client.
        :param sock: IP socket
        :return: None
        """
        if self._check_message_fields(request, ("username", "contact")):
            username = request.get("username")
            contact = request.get("contact")
            self.db.remove_user_contact(user=username, contact=contact)
            response = {
                "response_code": codes.c200_OK,
                "time": int(time.time()),
            }
        else:
            response = {
                "response_code": codes.c400_WRONG_REQUEST,
                "time": int(time.time()),
                "message": "Wrong message's fields"
            }

        self._logger.debug(f'Response del_contacts: "{response}"')
        self._responses[sock] = response

    def get_known_users_process(self, request: dict, sock) -> None:
        """
        A getting known users request handler.
         Message example:
         {
            "action": "get_known_users",
            "time": <unix timestamp>,
            "username": "username"
         }

        :param request: A message from a client.
        :param sock: IP socket
        :return: None
        """
        if self._check_message_fields(request, ("username",)):
            username = request.get("username")
            users = [user[0] for user in self.db.get_users_list()]
            response = {
                "response_code": codes.c202_ACCEPTED,
                "time": int(time.time()),
                "message": users
            }
        else:
            response = {
                "response_code": codes.c400_WRONG_REQUEST,
                "time": int(time.time()),
                "message": "Wrong message's fields"
            }

        self._logger.debug(f'Response get_known_users: "{response}"')
        self._responses[sock] = response

    def request_handler(self, request: dict, sock) -> None:
        """
        A general request handler.
         Determines the type of the request and calls the appropriate handler.
        :param request: A message from a client
        :param sock: IP socket
        :return: None
        """

        if self._check_message_fields(request, ("action", "time")):
            request_type = request.get('action')
            self._logger.debug(
                f'Received request type: "{request_type}", from: "{sock.getpeername()}"')

            if request_type == methods.AUTHENTICATE_1:
                self._logger.debug('Starting authenticate_1_process')
                self.authenticate_1_process(request, sock)

            elif request_type == methods.AUTHENTICATE_2:
                self._logger.debug('Starting authenticate_2_process')
                self.authenticate_2_process(request, sock)

            elif request_type == methods.PRESENCE:
                self.presence_process(request, sock)

            elif request_type == methods.PROBE:
                pass

            elif request_type == methods.MSG:
                self.message_process(request, sock)

            elif request_type == methods.QUIT:
                self.quit_process(request, sock)

            elif request_type == methods.JOIN:
                pass

            elif request_type == methods.LEAVE:
                pass

            elif request_type == methods.GET_CONTACTS:
                self.get_contacts_process(request, sock)

            elif request_type == methods.ADD_CONTACT:
                self.add_contacts_process(request, sock)

            elif request_type == methods.DEL_CONTACT:
                self.del_contacts_process(request, sock)

            elif request_type == methods.GET_KNOWN_USERS:
                self.get_known_users_process(request, sock)

            else:
                response = {
                    "response_code": codes.c400_WRONG_REQUEST,
                    "time": int(time.time()),
                    "message": "Unsupported action"
                }
                self._logger.debug(f'Response request_handler: {response}')
                self._responses[sock] = response

    def read_data(self, clients_to_read: list) -> None:
        """
        Read data from client which ready for read.

        :param clients_to_read: list of client ready for read
        :return: None
        """

        for sock in clients_to_read:
            try:
                data = sock.recv(system.MAX_PACKAGE_LENGTH).decode(system.ENCODING)
                request = json.loads(data)
                self._logger.debug(f'Received request: "{request}", from: "{sock.getpeername()}"')
                self.request_handler(request, sock)

            except Exception as err:
                self._logger.warning(f'A client {sock.getpeername()} disconnected.')
                self._clients.remove(sock)
                sock.close()

    def write_data(self, clients_to_write: list) -> None:
        """
        Write data to a client which ready for write.

        :param clients_to_write: list of client ready for write
        :return: None
        """

        for sock in clients_to_write:
            if sock in self._responses.keys():
                try:
                    resp = json.dumps(
                        self._responses[sock],
                        ensure_ascii=False).encode(
                        system.ENCODING)
                    self._logger.debug(f'A response: "{resp}"')
                    sock.send(resp)
                    self._logger.debug(
                        f'A response to the client: "{sock.getpeername()}", has been sent')
                except Exception:
                    self._logger.warning(f'A client {sock.getpeername()} disconnected')
                    self._clients.remove(sock)
                    sock.close()
                finally:
                    self._responses.pop(sock)

    def server_core(self) -> None:
        """
        Servers core side network process loop.

        :return: None
        """

        if self.transport:
            self._logger.warning(f'The server started on {self.address}:{self.port}')
            while True:
                try:
                    try:
                        client, _ = self.transport.accept()
                        self._logger.info(f'A connection has been accepted, from: "{client}"')
                    except OSError:
                        pass  # The socket timeout is out

                    else:
                        self._clients.append(client)

                    for username, sock in self._address_book.copy().items():
                        if sock not in self._clients:
                            self.db.user_logout(username=username)
                            if username in self._address_book.keys():
                                self._address_book.pop(username)
                            if username in self._session_crypts.keys():
                                self._session_crypts.pop(username)

                    try:
                        to_read, to_write, have_errors = select.select(
                            self._clients, self._clients, [], 10
                        )
                    except OSError:
                        pass  # Do nothing if some client disconnects

                    self.read_data(to_read)

                    if self._responses:
                        self.write_data(to_write)

                    time.sleep(system.TIMEOUT / 10)

                except KeyboardInterrupt:
                    self._logger.warning('KeyboardInterrupt. Exiting.')
                    sys.exit(0)

    def server_interactive(self) -> None:
        """
        A server's admin interactive process.
         Asks server's admin for commands and provide needed information.
        :return: None
        """

        while True:
            time.sleep(system.TIMEOUT)

            command = input('Please, enter command or "h" for help: ')

            if command == 'gu':
                print(self.db.get_users_list())
            elif command == 'ga':
                print(self.db.get_active_users_list())
            elif command == 'gh':
                username = input('Please, enter username: ')
                print(self.db.get_login_history(username))
            elif command == 'gmc':
                print(self.db.get_message_counter())
            else:
                print(
                    '\n h = help, \n gu = get all users, \n ga = get active users,'
                    ' \n gh = get history for username, \n gmc = get messages counters'
                )

    def user_disconnect(self, username: str) -> None:
        """
        Force disconnect user rom server

        :param username: str username
        :return: None
        """
        if username in self._address_book.keys():
            sock = self._address_book.pop(username)
            if sock and sock in self._clients:
                self._clients.remove(sock)

    def run(self) -> None:
        """
        Run the server loop

        :return: None
        """

        server_core = threading.Thread(target=self.server_core)
        server_core.daemon = True
        server_core.start()

        server_interactive = threading.Thread(target=self.server_interactive)
        server_interactive.daemon = True
        server_interactive.start()

        while True:
            time.sleep(system.TIMEOUT)
            if server_core.is_alive() and server_interactive.is_alive():
                continue
            break
