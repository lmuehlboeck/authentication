import sqlite3


def get_conn():
    """
    gets the database connection; creates database and tables if not existing
    
    :returns: database connection
    """
    conn = sqlite3.connect("data.db")
    # create database and tables if they do not exist
    with open("schema.sql") as f:
        conn.executescript(f.read())
    return conn


def execute_query(conn, query, args=()):
    """
    executes a SQL query

    :param conn: database connection
    :param query: the SQL query to be executed
    :param args: arguments for the SQL query as tuple, are replaced for '?'
    :returns: result of SQL query, None in case of an error
    """
    try:
        cur = conn.execute(query, args)
        res = cur.fetchall()
        conn.commit()
        cur.close()
        return res if res else []
    except Exception as e:
        print("SQL query could not be executed: " + str(e))
        return None