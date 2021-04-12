import sqlite3
import re

conn = sqlite3.Connection("user-db.db")

# this code is to insert data into the table


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

    for row in rows:
        print(row)

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

# code to create a Table


def create_table(conn):
    c.execute("""
		CREATE TABLE customers (
		  first_name text,
		  last_name text,
		  email text)
    """)


# insert_by_slot(conn,
#                slot_name=('name', 'email'),
#                slot_value=('Gaurav', 'jeetu123@gmail.com')
#                )
# select_by_slot(conn,
#                slot_name="name",
#                slot_value="Raj"
#                )

# select_all(conn)

# Make a regular expression
# for validating an Email
regex = '^(\w|\.|\_|\-)+[@](\w|\_|\-|\.)+[.]\w{2,3}$'

# Define a function for
# for validating an Email


def check(email):

    # pass the regular expression
    # and the string in search() method
    if(re.search(regex, email)):
        print("Valid Email")

    else:
        print("Invalid Email")


email = "uddaishya@ibm.org"
check(email=email)
conn.close()
