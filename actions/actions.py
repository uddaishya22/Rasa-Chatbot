# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


from typing import Any, Text, Dict, List, Union

from rasa_sdk import Action, Tracker, FormValidationAction
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.types import DomainDict

import sqlite3
from rasa_sdk.events import SlotSet

import re
regex = '^(\w|\.|\_|\-)+[@](\w|\_|\-|\.)+[.]\w{2,3}$'


class ValidateUserInfoForm(FormValidationAction):

    def name(self) -> Text:
        return "validate_user_info_form"

    def validate_PERSON(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict
    ) -> Dict[Text, Any]:

        print(
            f"Name given by user is {slot_value} and have length of {len(slot_value)}")
        if len(slot_value) <= 2:
            dispatcher.utter_message(
                text="That's very short name. I'm assuming you mis-spelled.")
            return {"PERSON": None}
        else:
            return {"PERSON": slot_value}

    def validate_email(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict
    ) -> Dict[Text, Any]:

        print(f"\nEmail provided is {slot_value}")
        verify_mail = DbQueryingMethods.check_mailid(slot_value)
        if verify_mail == True:
            return {"email": slot_value}
        else:
            dispatcher.utter_message(text="Please, Enter a valid mail id.")


class ActionQuerySubscription(Action):

    def name(self) -> Text:
        return "action_query_subscription"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        conn = DbQueryingMethods.create_connection("user-db.db")

        slot_value = tracker.get_slot("email")
        slot_name = "email"

        if not slot_value:
            dispatcher.utter_message(text="Please enter your email")

        else:
            get_query_results = DbQueryingMethods.select_by_slot(conn=conn,
                                                                 slot_name=slot_name,
                                                                 slot_value=slot_value)

            dispatcher.utter_message(text=f"Results : {get_query_results} ")
        conn.close()
        return []


class ActionInsertInfo(Action):

    def name(self) -> Text:
        return "action_insert_info"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        PERSON = tracker.get_slot("PERSON")
        email = tracker.get_slot("email")

        conn = DbQueryingMethods.create_connection("user-db.db")

        slot_value = (PERSON, email)
        slot_name = ('name', 'email')

        insert_user_info = DbQueryingMethods.insert_by_slot(conn=conn,
                                                            slot_name=slot_name,
                                                            slot_value=slot_value)
        dispatcher.utter_message(text=f"{PERSON} succesfully subscribed !!!")
        conn.close()
        return []

# for showing the list of users


class ActionUserList(Action):

    def name(self) -> Text:
        return "action_user_list"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        conn = DbQueryingMethods.create_connection("user-db.db")

        user_rows = DbQueryingMethods.select_all(conn=conn)
        for row in user_rows:
            dispatcher.utter_message(
                text=f"\n==> Name: {row[0]}\t\t| Mail-id: {row[1]}")
            print(row)

        conn.close()
        return []


class DbQueryingMethods:

    # Define a function for
    # for validating an Email
    def check_mailid(email):

        # pass the regular expression
        # and the string in search() method
        if(re.search(regex, email)):
            print("\nValid")
            return True

        else:
            print("\nInvalid mail")
            return False

    def create_connection(db_file):
        """ 
        create a database connection to the SQLite database
        specified by the db_file
        :param db_file: database file
        :return: Connection object or None
        """
        conn = None
        try:
            conn = sqlite3.connect(db_file)
        except Error as e:
            print(e)

        return conn

    def insert_by_slot(conn, slot_name, slot_value):
        c = conn.cursor()
        c.execute(f"""
            INSERT INTO user_info {slot_name} VALUES {slot_value};
        """)
        conn.commit()

    # creating a function for fetching a data by slot

    def select_by_slot(conn, slot_name, slot_value):
        c = conn.cursor()

        c.execute(f"""
            SELECT * FROM user_info WHERE {slot_name} == '{slot_value}';
        """)

        rows = c.fetchall()
        if rows == []:
            return "Sorry, No results found with this email!!!"
        else:
            return [rows]

        conn.commit()

    # creating a function for fetching data from table

    def select_all(conn):
        c = conn.cursor()

        c.execute(f"""
            SELECT * FROM user_info;
        """)

        return c.fetchall()

        for row in rows:
            print(row)

        conn.commit()
