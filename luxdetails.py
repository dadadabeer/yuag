"""
Module for displaying details from the Lux Database.
"""
import argparse
import sys
from contextlib import closing
from sqlite3 import connect, DatabaseError, Error
from object import Object

DATABASE_URL = 'file:lux.sqlite?mode=ro'

def main():
    """Main function to display object details."""
    parser = argparse.ArgumentParser(allow_abbrev=False)
    parser.add_argument('id', nargs=1, type=int,
                        help="The ID of the object whose details should be shown")
    args = parser.parse_args()
    object_id = args.id[0]

    try:
        with connect(DATABASE_URL, isolation_level=None, uri=True) as conn:
            with closing(conn.cursor()) as cur:
                # validate_id(object_id, cur)
                display_summary(object_id, cur)
                display_label(object_id, cur)
                display_production_details(object_id, cur)
                display_classifications(object_id, cur)
                display_references(object_id, cur)

    except DatabaseError as db_err:
        print(f"Database Error: {db_err}", file=sys.stderr)
        sys.exit(1)

    except Error as e_err:
        print(f"Error: {e_err}", file=sys.stderr)
        sys.exit(1)

def display_summary(object_id, cur):
    """Display summary of the object identified by the given ID."""
    query = '''
        SELECT 
            objects.accession_no,
            objects.date,
            GROUP_CONCAT(places.label, ', ') AS places,
            departments.name AS department_name
        FROM 
            objects
        LEFT JOIN 
            objects_places ON objects.id = objects_places.obj_id
        LEFT JOIN 
            places ON objects_places.pl_id = places.id
        LEFT JOIN 
            objects_departments ON objects.id = objects_departments.obj_id
        LEFT JOIN 
            departments ON objects_departments.dep_id = departments.id
        WHERE 
            objects.id = ?
        GROUP BY 
            objects.id
    '''

    cur.execute(query, (object_id,))
    result = cur.fetchall()
    # headers = ["Accession Number", "Date", "Places", "Department"]

    # return Table(headers, result)
    return result

# def print_title_table(title):
#     """Print a title table with the given title."""
#     # print(Table([title], [[' ']]))

# def return_title_table(title):
#     """Print a title table with the given title."""
#     # return Table([title], [[' ']])

def display_label(object_id, cur):
    """Display label of the object identified by the given ID."""
    query = 'SELECT label FROM objects WHERE objects.id = ?'
    cur.execute(query, (object_id,))
    result = cur.fetchone()
    # if result:
    #     table = Table(['Label'], [[result[0]]])
    #     return table
    #     return "No label found for the provided Object ID."
    return result

def display_production_details(object_id, cur):
    """Display production details of the object identified by the given ID."""
    query = '''
        SELECT
            productions.part,
            agents.name,
            agents.begin_date,
            agents.end_date,
            GROUP_CONCAT(nationalities.descriptor, '\n') AS nationalities
        FROM
            productions
        INNER JOIN
            agents ON productions.agt_id = agents.id
        LEFT JOIN
            agents_nationalities ON agents.id = agents_nationalities.agt_id
        LEFT JOIN
            nationalities ON agents_nationalities.nat_id = nationalities.id
        WHERE 
            productions.obj_id = ?
        GROUP BY 
            productions.part, agents.name, agents.begin_date, agents.end_date
        ORDER BY 
            agents.name ASC, productions.part ASC, nationalities.descriptor ASC
    '''

    cur.execute(query, (object_id,))
    results = get_production_results(cur)
    # headers = ["Part", "Name", "Nationalities", "Timespan"]
    # return Table(headers, results)
    return results

def get_production_results(cur):
    """Get production results from the cursor."""
    initial_results = cur.fetchall()
    results = []
    for row in initial_results:
        beginning_year = str(row[2].split('-')[0]) if row[2] else ''
        ending_year = str(row[3].split('-')[0]) if row[3] else ''
        timespan = beginning_year + '' + ending_year if ending_year else beginning_year + ''
        results.append((row[0], row[1], row[4], timespan))

    # if not results:
    #     results = [["-", "No Production Details found", "-", "-"]]
    return results

def display_classifications(object_id, cur):
    """Retrieve and display classifications of the object identified by the given ID."""
    query = ('SELECT GROUP_CONCAT(classifiers.name, ", ") '
             'FROM objects_classifiers '
              'LEFT JOIN classifiers ON objects_classifiers.cls_id = classifiers.id '
              'WHERE objects_classifiers.obj_id = ? '
              'GROUP BY objects_classifiers.obj_id '
              'ORDER BY classifiers.name ASC')

    cur.execute(query, (object_id,))
    result = cur.fetchall()
    class_data = []

    if result and result[0][0]:
        classifications = result[0][0].split(", ")
        class_data = list(classifications)
    # else:
    #     class_data = [["No Classification found"]]
    capitalized_data = [element.capitalize() for element in class_data]
    capitalized_data.sort()
    print(capitalized_data)

    # table = Table(['Classified As'], class_data)
    return capitalized_data


def display_references(object_id, cur):
    """Display reference information of the object identified by the given ID."""
    query = '''
            SELECT "type", "content" 
            FROM "references" 
            WHERE obj_id = ?
            ORDER BY id
            '''

    cur.execute(query, (object_id,))
    result = cur.fetchall()
    # headers = ["Type", "Content"]

    if not result:
        return "No data found"
    return result


def fetch_data(query, object_id, cur):
    """Execute a given query and return the result."""
    cur.execute(query, (object_id,))
    return cur.fetchall()

def format_entry_results2(object_id):
    """
    Retrieve detailed information about an object from the database based on the given object_id.

    This function establishes a connection to the database and fetches various details about
    the object corresponding to the provided object_id. The details include summary, label,
    production details, classifications, and references.

    Args:
        object_id (int): The unique identifier of the object for which the details are to get.

    Returns:
        Object: An instance of the Object class populated with the retrieved details.

    Raises:
        Any exceptions raised during database connection, query execution, data retrieval, or
        object instantiation will be propagated.

    Note:
        The database connection and cursor are closed automatically after execution due
        to the use of context managers.

    Example:
        result_obj = format_entry_results2(1234)
    """
    # create a connection to the database
    with connect(DATABASE_URL, isolation_level=None, uri=True) as connection:
        # create a cursor for the database
        with closing(connection.cursor()) as cur:

            # Validate object ID
            # validate_id(object_id, cur)

            # Dictionary to store data retrieval functions and their respective labels
            data_retrieval_functions = {
                'summary': display_summary,
                'label': display_label,
                'prod': display_production_details,
                'classifications': display_classifications,
                'ref': display_references
            }

            # Dictionary to store results
            results = {}

            for key, function in data_retrieval_functions.items():
                results[key] = function(object_id, cur)

            #error handling if object id does not exist
            if not results.get('summary'):
                return None

            # Extract values from the results dictionary
            acc_no, date, place, dep = results['summary'][0]
            label = results['label'][0]
            prod = results['prod']
            classifications = results['classifications']
            ref = results['ref']

            obj = Object(obj_id=object_id, acc_no=acc_no, date=date, place=place, dept=dep,
                        label=label, productions=prod, classifiers=classifications, references=ref)

            return obj
