"""This module provides a command line interface for querying the YUAG database.
It takes in arguments from the command line and returns a table of results.
Usage: python lux.py [-d date] [-a agent] [-c classifier] [-l label]"""
from sys import stderr, exit as sys_exit
from contextlib import closing
from sqlite3 import connect
from object import Object

DATABASE_URL = 'file:lux.sqlite?mode=ro'

def get_filter_terms(args):
    """Creates a filter string and a dictionary of parameters based on the arguments passed in.
    Args:
        args: The arguments passed in from the command line.
    Returns:
        filters (string): The filter string to be used in the query.
        params (dict): The parameters for the query.
    """

    filters = " WHERE 1=1"
    params = {}
    if args.a:
        filters += ' AND agents.name LIKE :a'
        params['a'] = f"%{args.a.lower()}%"

    if args.c:
        filters += ' AND classifiers.name LIKE :c'
        params['c'] = f"%{args.c.lower()}%"

    if args.d:
        filters += ' AND date LIKE :d'
        params['d'] = f"%{args.d}%"

    if args.l:
        filters += ' AND label LIKE :l'
        params['l'] = f"%{args.l}%"
    return filters, params

def get_filters(label, classification, agent, date):
    """Creates a filter string and a dictionary of parameters based on the arguments passed in.
    Args:
        args: The arguments passed in from the command line.
    Returns:
        filters (string): The filter string to be used in the query.
        params (dict): The parameters for the query.
    """

    filters = " WHERE 1=1"
    params = {}
    if agent:
        filters += ' AND agents.name LIKE :a'
        params['a'] = f"%{agent.lower()}%"

    if classification:
        filters += ' AND classifiers.name LIKE :c'
        params['c'] = f"%{classification.lower()}%"

    if date:
        filters += ' AND date LIKE :d'
        params['d'] = f"%{date}%"

    if label:
        filters += ' AND label LIKE :l'
        params['l'] = f"%{label.lower()}%"
    return filters, params

def create_query(filters):
    """Creates a query based on the filters passed in.
    Args:
        filters (string): The filter string to be used in the query.
    Returns:
        query (string): The query to be executed.
    """

    # retrieve the objects that match the filters
    objects = "SELECT DISTINCT"
    objects += " objects.id as object_id, objects.label as label, objects.date as date FROM objects"
    objects += " join productions ON objects.id = productions.obj_id"
    objects += " join agents ON productions.agt_id = agents.id"
    objects += " join objects_classifiers ON objects.id = objects_classifiers.obj_id"
    objects += " join classifiers ON objects_classifiers.cls_id = classifiers.id"
    objects += filters

    # create agent info column as a concatenation of agent names and parts
    agents = "SELECT"
    agents += " object_id as agent_id, label,"
    agents += " GROUP_CONCAT(DISTINCT names || ' (' || parts || ')|') as agent_info, date FROM"
    agents += " (SELECT object_id, label, agents.name as names, productions.part as parts, date"
    agents += " FROM ({}) LEFT join productions ON object_id = productions.obj_id".format(objects)
    agents += " LEFT join agents ON productions.agt_id = agents.id"
    agents += " ORDER BY LOWER(names), LOWER(parts))"
    agents += " GROUP BY object_id"

    # create classifiers column as a concatenation of classifier names
    classifiers = "SELECT object_id as classifier_id, GROUP_CONCAT(DISTINCT class || '|') as class"
    classifiers += " FROM (SELECT object_id, LOWER(classifiers.name) as class"
    classifiers += " FROM ({}) join".format(objects)
    classifiers += " objects_classifiers ON object_id = objects_classifiers.obj_id"
    classifiers += " join classifiers ON objects_classifiers.cls_id = classifiers.id"
    classifiers += " ORDER BY LOWER(class))"
    classifiers += " GROUP BY object_id"

    # join the tables and order the results
    query = "SELECT agent_id, label, agent_info, date, class FROM ({})".format(agents)
    query += " JOIN ({}) ON agent_id=classifier_id".format(classifiers)
    query += " ORDER BY label, date"
    query += " LIMIT 1000"
    return query

def execute(query, params):
    """Executes the query and returns the rows.
    Args:
        query (string): The query to be executed.
        params (dict): The parameters for the query.
    Returns:
        rows (list): The results of the query.
    """

    try:
        with closing(connect(DATABASE_URL, uri=True)) as conn:
            with closing(conn.cursor()) as cur:
                cur.execute(query, params)
                rows = cur.fetchall()
                return rows

    except Exception as error:
        print(error, file=stderr)
        sys_exit(1)

def format_query_results(rows):
    """Formats the results of the query.
    Args:
        rows (list): The results of the query.
    Returns:
        None
    """

    res = []
    for row in rows:
        row = list(row)
        if row[2] is None:
            row[2] = ""
        if row[-1] is None:
            row[-1] = ""
        row[2] = row[2].replace('|,', ',')[:-1]
        row[-1] = row[-1].replace('|,', ',')[:-1]
        row[2], row[3] = row[3], row[2]
        res.append(tuple(row))
    return res



def search(label=None, classification=None, agent=None, date=None):
    """
    Search the database for objects based on given criteria to return a list of Object instances.

    Make a query based on the provided filtering criteria (label, classification, agent, and date).
    It then executes the query and processes each row of the result to create an instance of Object.
    The resulting list of Object instances is then returned.

    Args:
        label (str, optional): Label to search by. Defaults to None.
        classification (str, optional): Classification to search by. Defaults to None.
        agent (str, optional): Agent to search by. Defaults to None.
        date (str, optional): Date to search by. Defaults to None.

    Returns:
        list[Object]: A list of Object instances containing the search results.

    Raises:
        Any exception raised during database connection or query execution.

    Example:
        result = search(label="ExampleLabel", agent="JohnDoe")
    """
    def process_row(row):
        agents = (row[2] or "None").rstrip('|').split('|')
        classifiers = (row[4] or "None").rstrip('|').split('|')

        return Object(
            obj_id=int(row[0]),
            label=str(row[1]),
            date=str(row[3]),
            agents=agents,
            classifiers=classifiers
        )

    object_list = []
    filters, params = get_filters(label, classification, agent, date)
    query = create_query(filters)
    try:
        with connect(DATABASE_URL, uri=True) as connection:
            with closing(connection.cursor()) as cursor:
                cursor.execute(query, params)
                rows = cursor.fetchall()
                object_list.extend(map(process_row, rows))
    except Exception as error:
        print(error, file=stderr)
        sys_exit(1)

    return object_list
