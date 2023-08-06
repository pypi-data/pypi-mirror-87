"""
JIM protocol methods
"""

# The Service message for notifying the server about the presence of the client online
PRESENCE = 'presence'
# The Service message from the server to check the presence of the client online
PROBE = 'probe'
# A simple message to a user or a chat
MSG = 'msg'
# A disconnection from a server
QUIT = 'quit'
# An authorization of client on a server
AUTHENTICATE_1 = 'authenticate_1'
AUTHENTICATE_2 = 'authenticate_2'
# Join a chat
JOIN = 'join'
# Leave a chat
LEAVE = 'leave'
# Get contacts
GET_CONTACTS = "get_contacts"
# Add contact
ADD_CONTACT = "add_contact"
#  Delete contact
DEL_CONTACT = "del_contact"
# Get known users
GET_KNOWN_USERS = "get_known_users"