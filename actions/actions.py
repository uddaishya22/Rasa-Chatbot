# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

import sqlite3
from rasa_sdk.events import SlotSet


class ActionQuerySubscription(Action):

    def name(self) -> Text:
        return "action_query_subscription"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        conn = DbQueryingMethods.create_connection("user-db.db")

        slot_value = tracker.get_slot("email")
        slot_name = "email"

        # if not slot_value:
        #     dispatcher.utter_message(text=f"Enter your {slot_name} ")

        get_query_results = DbQueryingMethods.select_by_slot(conn=conn,
                                                             slot_name=slot_name,
                                                             slot_value=slot_value)

        dispatcher.utter_message(text=f"Results : {get_query_results} ")
        conn.close()
        return []


class DbQueryingMethods:

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

        rows = c.fetchall()

        for row in rows:
            print(row)

        conn.commit()
