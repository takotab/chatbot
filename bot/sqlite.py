import os
import sqlite3
import sys
import json
import argparse

# Query print request


def print_request(table_name, target, to_show, c, c_names):
    print("target", target, "table_name = ", table_name)
    d = dict(json.loads(target.replace("'", "\"")))
    l = [" {}='{}' AND".format(data, column_name)
         for data, column_name in d.items()]
    l[-1] = l[-1].replace("AND", " ")
    sql_query = "SELECT * FROM {} WHERE {}".format(
        "\'" + table_name + "\'", "".join(l))
    print(sql_query)
    # Execute query
    c.execute(sql_query)
    all_rows = c.fetchall()
    print("debug all rows", all_rows)
    return_data = ""
    if len(all_rows) == 1:
        for row in all_rows:
            return_data += "{}".format(row[c_names[to_show]])
    elif len(all_rows) > 1:
        return_data += "0"
    else:
        print("Command used:\n{}\n".format(sql_query))
        print("0 records found.")
        return_data += "0"
    return return_data
# Query print change request


def change_request(table_name, target_id, target_change, c, c_names, conn):
    print("data = ", target_id, "target = ",
          target_change, "table_name = ", table_name)
    # Create query for SQL DB
#     d = dict(json.loads(target.replace("'", "\"")))
#     l = [" {}='{}', ".format(data, column_name) for data, column_name in d.items()]
#     l[-1] = l[-1].replace(",", " ")

    sql_change = "UPDATE {} SET {} WHERE {}=\'{}\'".format(
        table_name, target_change, "sql_id", target_id)
    print(sql_change)
#     try:
    c.execute(sql_change)
    conn.commit()
#     except:
#         print("Commit error happend!")


def do_stuff(action, data, target):
    table_name = "head"  # this is table that we are working on
    # name of the sqlite database file
    sqlite_file = os.path.join("sqlite", "random_table_dwg.db")
    print(sqlite_file)
    # Connect to database
#     create_engine('sqlite:///{}'.format(xxx), connect_args={'timeout': 15})
    conn = sqlite3.connect(sqlite_file)
    c = conn.cursor()
    # Create list of columns to use latter
    c.execute("PRAGMA table_info({})".format(table_name))
    c_names = {r[1]: r[0] for r in c.fetchall()}
    if action == "print":
        target_print = str(data)
        #to_show = c_names[target]
        to_show = str(target)
        return print_request(table_name, target_print, to_show, c, c_names)
        conn.close()
    elif action == "change":
        target_id = data
        target_change = target
        change_request(table_name, target_id, target_change, c, c_names, conn)
        conn.close()
    else:
        print("Execute command with -h to see examples.")


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Manipulate Database SQLite \n',
                                     formatter_class=argparse.RawDescriptionHelpFormatter,
                                     epilog='''print example:
\tpython functions.py --action print --target CITY --data "{\'FIRST_NAME\':\'Floris\', \'LAST_NAME\':\'Diepen\', \'DOB\':24}"\n\n
change example:
\tpython functions.py --action change --target 1 --data "{\'CITY\':\'Amsterdam\'}"

''')
    parser.add_argument('--action', choices=['change', 'print'],
                        help='Choose action print or change\n', required=True)
    parser.add_argument('--target', nargs='?', help='if print action is used - which field to output for given search\n'
                                                    'if change action is used - which user_id to chamge\n', required=True)
    parser.add_argument('--data', nargs='?', help='if print action is used - what  data to use for search\n '
                                                  'if change action is used - what data to change\n', required=True)

    args = parser.parse_args()
    do_stuff(args.action, args.data, args.target)
    # ------------------------------------------------------------------------------------------------------------------
