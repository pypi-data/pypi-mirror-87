"""EATERYWEBSOCKET.PY
This library implement a main interface for interfacing with the Lunchbot websocket API.
It is utilized by the EateryNod file that implements the parsing etc."""

from threading import Thread #Import Thread
import websocket, json #Import the required libraries
from .Exceptions import InvalidSubscriptionType #Import the exceptions used by this file

class EaterySocket(object):
    """Defines the main socket class. The basic concepts is that the socket will run threaded
    and, when it recieves a message, follow this flow:
    =>Message recieved=>Parse JSON=>Call EateryNod.parse_menu()=>Provide a callback to a desired function."""

    def __init__(self, menu, subscribe_to, log=False):
        """The initialization function. Takes two attributes, the menu object that the socket relates to,
        and the school food events that should be subscribed to"""
        self.menu = menu #Map function args to self variables
        self.available = False #Set the value that shows the availability of the menu to False
        self.subscribe_to = subscribe_to #Map function args to self variables
        #Create a websocket object
        if log: websocket.enableTrace(True) #Enable trace for the websocket if logging has been enabled via the initialize function.
        self.ws_connection = websocket.WebSocketApp("wss://eatery.nero2k.com/ws", on_data=self.on_data) #Create the websocket app with on_data as the callback function
        self.ws_connection.on_open = self.on_initialization #Map the on_initailization function to the on_open trigger (it will be triggered when the socket has been initialized)
        wst = Thread(target=self.ws_connection.run_forever) #Create a thread where the websocket will run in
        wst.daemon = True #Enable daemon for the thread
        wst.start() #Start the thread

    def generate_subscription_payload(self, subscribe_to):
        """A simple function for generating a subscription payload.
        The subscribe_to argument takes a list ["2020-09"], or the string "all" or "latest"."""
        if type(subscribe_to) == str and subscribe_to.lower() not in ["all", "latest"] or type(subscribe_to) not in [str, list, None]: #If a string is provided, but it seems invalid, or the type provided is invalid,
            raise InvalidSubscriptionType("""The provided subscription type is invalid. Try with "all".""")
        return json.dumps({"action": "menu_update_request", "subscribe_to": [subscribe_to] if type(subscribe_to) != list else subscribe_to}) #Generate the payload. Use a simple if statement to wrap the subscribe_to into a list in case it has not been provided as a list,

    def generate_test_payload(self):
        """A simple function for generating the test payload to test the connection."""
        return json.dumps({"action": "menu_update_test"}) #Send the "menu_update_test" action to get the initial menu

    def on_data(self, message, *args):
        """Function to call when data has been recieved"""
        data = json.loads(message)["message"] #First, convert the data to JSON
        converted_data = self.menu.update_menu(data) #Send the updated data to the parent menu object

    def on_initialization(self):
        """Function that will be called when the websocket has been initialized."""
        self.available = True #Set the available variable to True to indicate that the websocket is ready.
        if self.subscribe_to != None: self.ws_connection.send(self.generate_subscription_payload(self.subscribe_to)) #Subscribe to the configured events if the decision to subscribe to events has been made.
        self.ws_connection.send(self.generate_test_payload()) #Send a test payload to get the current week menu