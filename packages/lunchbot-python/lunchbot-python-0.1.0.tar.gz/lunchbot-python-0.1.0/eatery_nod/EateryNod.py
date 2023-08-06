"""EATERY.PY
One of two main files for the Python Eatery API.

This library currently supports parsing Eatery API JSON.
It is based on the Nero2K Lunchtbot WebSocket API, although this file only
contains the parsing functions, and communicates with EaterySocket.py, which does all the
data-retrieving."""

import requests, datetime, time, pytz #Import the required libraries for running the library
from .EateryWebsocket import EaterySocket #Import the EaterySocket file for interfacing with WebSockets.
from .Exceptions import RetrievalTimeout, InitializationTimeout #Import the exceptions used by this file

class Menu(object):
    """Define the Menu class. The main thing you want from this class is the
    entries parameter, which contains parsed menu items."""

    def __init__(self):
        """The initalizing class for a menu. Takes no arguments and returns variables utilized by the class,
        with the ones that has information yet to be retrieved set to None, except entries that is set to an empty list.
        In this inialization class,"""
        self.entries = None #Define the list for storing the menu entries.
        self.image = {"raw": None, "ocr": None} #Define the variable for the menu image
        self.week = None #The week number for the menu
        self.retrieved_week = None #The week number when the menu was retrieved
        self.schema_version = None #The API schema version
        self.menu_json = None #The menu JSON as sent by the API
        self.last_retrieved = {"image": {"raw": None, "ocr": None}, "json": None} #This variable implements a simple cache, se the retrieve_menu_image function.
        self.menu_last_sent = None #Stores when the menu was last sent to the user - used by the wait_for_update function

    def initialize(self, subscribe_to="all", log=False):
        """An initializaion function that needs to be called by the user manually before initializing a WebSocket session.
        This function is implemented so that the user can call other implemented APIs besides the WebSocket API."""
        self.socket = EaterySocket(self, subscribe_to, log) #Create a socket object for the menu
        self._wait_for_connect(30) #Wait for the web socket to connect with a timeout of 60 seconds

    def retrieve_menu_image(self, force_request=False, ocr_image=False):
        """Function for retrieving the menu image from the Lunchbot API, or from the stored cache in the self.menu_image variable.
        The image will be returned as a file."""
        now = datetime.datetime.now()  #Store the current time, just temporarily.
        image_type = "ocr" if ocr_image else "raw" #The type of the image, for integrating with the last_retrieved variable.
        last_retrieved = self.last_retrieved["image"][image_type] #Get when the image was last retrieved
        if last_retrieved == None or last_retrieved.isocalendar()[1] != now.isocalendar()[1] or force_request:
            #If the menu image has not been retrieved (self.last_retrieved == None or it has not been retrieved this week) or if the force_request variable has been set to True
            self.image[image_type] = requests.get("https://eatery.nero2k.com/api/image%s"%("/ocr" if ocr_image else "/")).content #Make a request to either the raw image or the OCR image API depending on the user's option.
            self.last_retrieved["image"][image_type] = now  # Update the time for when the menu image was last retrieved.
        return self.image[image_type] #Return the menu image

    def update_menu(self, menu_json):
        """Function for parsing and updating the menu. Takes the menu JSON returned by retrieve_menu and returns individual Day objects that
        are appended to the Menu's entry list."""
        self.menu_json = menu_json
        self.week = self.menu_json["actual_week"]  # Get the week number for when the menu is applicable for
        self.retrieved_week = self.menu_json["iteration_week"]  # Get the week number for when the menu was retrieved. This week number should not be used for displaying the actual menu week number
        self.schema_version = self.menu_json["schema_version"]  # Get and save the schema version of the API response.
        self.last_retrieved["json"] = datetime.datetime.now() #Update when the menu was last retrieved
        entries = [] #Create a list to store the menu entries in. We don't use the self.entries variable directly, just in case something would go wrong in the parsing.
        for day, menu_items in menu_json["menu"].items(): #Loop through the days
            entries.append(Day(menu_items, day)) #Create a day object and add it to the list of menu items
        self.entries = entries #Update the parsed menu
        return self.entries #Return the parsed menu.

    def _wait_for_menu(self, timeout=None):
        """This function waits until a menu is retrieved. It is not recommended to call this one directly,
        use get_menu() instead."""
        seconds = 0 #Count how many seconds that have passed waiting
        while self.entries == None:
            time.sleep(0.1)
            if timeout: #Check if a timeout has been configured
                seconds += 0.1 #Increase the second counter
                if seconds > timeout: raise RetrievalTimeout("The timeout of {} seconds was exceeded while waiting for menu data.".format(timeout)) #If the timeout has been passed, raise an exception

    def _wait_for_connect(self, timeout=None):
        """This function waits until the websocket API has connected"""
        seconds = 0 #Count how many seconds that have passed waiting
        while self.socket == None or self.socket.available == False:
            time.sleep(0.1)
            if timeout: #Check if a timeout has been configured
                seconds += 0.1 #Increase the second counter
                if seconds > timeout: raise InitializationTimeout("The timeout of {} seconds was exceeded while waiting for the connection to be initialized.".format(timeout)) #If the timeout has been passed, raise an exception

    def get_menu(self, image=False, image_type="raw", force_request=False, timeout=30):
        """Function for retrieving and parsing the menu.
        Takes three arguments, all boolean (except image_type, which is str):
        Image - wheteher a menu image should be returned or not
        Image_type - The type of the image to be retrieved, OCR och Raw.
        Force_request - (only applicable for the image endpoint) - whether a request should be forced or not.
        Timeout - (only applicable for the JSON menu) - a timeout if we have to wait for the menu to be retrieved."""
        if image: #If the menu image has been set to be retrieved
            return self.retrieve_menu_image(force_request=force_request, ocr_image=(True if image_type == "ocr" else False)) #Return the menu image
        else: #If we should not return an image
            menu_last_retrieved = self.last_retrieved["json"] #Get when the menu was last retrieved
            now = datetime.datetime.now()  # Store the current time, just temporarily.
            self.menu_last_sent = menu_last_retrieved #Save when the user last called  this function and got data
            updated_this_week = False if menu_last_retrieved == None or menu_last_retrieved.isocalendar()[1] != now.isocalendar()[1] else True
            if self.entries != None and updated_this_week: #If the menu has been updated this week.
                return self.entries
            else:
                self._wait_for_menu(timeout)
                return self.entries #Return the menu if it has been gotten and if it has been updated this week.
            #^If not, wait for the next menu

    def wait_for_menu_update(self):
        """Function for waiting until a menu update is sent.
        It utilizes the menu_last_sent-variable to check if the menu has been updated
        since the user last retrieved menu data."""
        while self.menu_last_sent == self.last_retrieved["json"]:
           time.sleep(1)

class Day(object):
    """Define the Day class, which represents a day with individual menu items.
    This library also comes with some neat parsing functions - that's always tasty (just like Eatery) :)."""

    def __init__(self, menu_items, day_name):
        """Initalizing function for the Day object. Takes a list of the menu items for that day, and a day name like 'monday',
        and returns that and several other nice parameters."""
        self.menu_items = menu_items #A list of the menu items for the particular day.
        self.day_name = str(day_name).capitalize() #The pure name of the day, e.g. Monday.
        self._day_names_swedish = {"Monday": "Måndag", "Tuesday": "Tisdag", "Wednesday": "Onsdag", "Thursday": "Torsdag", "Friday": "Fredag"} #Day name mappings from English to Swedish,
        self.day_name_sv = self._day_names_swedish[self.day_name] #Get the day name in Swedish
        now = datetime.datetime.now() #Store the current time, just temporarily.
        self.day_start = (now - datetime.timedelta(days=now.weekday() - list(self._day_names_swedish.keys()).index(self.day_name))).astimezone(pytz.timezone("Europe/Stockholm"))
        #Now that above line might seem confusing, but it really is simple.
        #1. Get the current day date
        #2. Subtract it with the amount of days that are between today and the listed day. We do that by first getting the current weekday number (this will be from 0-6), but
        #0-4 here because we're only dealing with week menus. And then, we subtract the current weekday with the index of today's date in the dict containg day names as keys, to get
        #the equivalent weekday number of the day. This will give the correct day date as an output.
        #Last, we covert it to the timezone in Sweden.

        #Now, we have the correct date. We want the following timestamps, some which are included just for the sake of that more data = more fun:
        #1. The start of the day (00:00). We do that by getting the initial day_start timestamp right.
        self.day_start.replace(hour=0, minute=0, second=1, microsecond=1) #This timestamp will be the reference for everything else.
        #2. The end of the day (23:59)
        self.day_end = self.day_start #Clone the day_start variable
        self.day_end.replace(hour=23, minute=59, second=59, microsecond=999999)
        #3. The day date
        self.day_date = self.day_start.date() #Use the date from the day_start timestamp.
        #The start of the Eatery lunch service (NOTE: this is generally. Times may be different and vary.)
        self.service_start = self.service_end = self.day_start #Copy the day_start variable again
        #As of 2020-10-22, Eatery stated that their lunch opening times were 10:30 - 14:00 on https://eatery.se/kista-nod/.
        self.service_start.replace(hour=10, minute=30) #Adjust to get the right timings. The second and microsecond will already be 1, we don't have to to anything about that.
        self.service_end.replace(hour=14) #Adjust to get the right timings. The second and microsecond will already be 1, and the minute will be 0 we don't have to to anything about that.
        #----------
        #Get if a dessert, pancakes, or burgers are listed for the day as an extra bonus. Here, we could just assume that every tuesday is sweet tuesday, and so on, but we implement
        #super-simple parsing just to make sure.
        self._menu_items_joined = " ".join(self.menu_items).upper() #We join the list of menu items into a string so we can perform the checks below. We also convert it to uppercase only to make sure that some parsing functions will work.
        self.dessert_served = True if "SWEET" in self._menu_items_joined else False #This will return True if the string SWEET is in any of the menu items (e.g. "SWEET TUESDAY: Vi bjuder på något gott efter maten.")
        self.pancakes_served = True if any(string in self._menu_items_joined for string in ["PANCAKE", "PANNCAKE", "PANNKAKOR"]) else False #This will return True if the string PANCAKE, PANNCAKE or Pannkakor is in any of the menu items (e.g. "PANNCAKE THURSDAY: Pannkakor med nykokt sylt och grädde ingår till alla som äter lunch!")
        self.burgers_served = True if any(string in self._menu_items_joined for string in ["BURGER", "BURGARE"]) else False #This will return True if the string BURGER or burgare is in any of the menu items (e.g. "BURGER FRIDAY- Eaterys högrevsburgare eller portabellaburgare med massa goda tillbehör!")
        #^If you eat in the Campus part of Eatery, it is not guaranteed that you will be served burgers.