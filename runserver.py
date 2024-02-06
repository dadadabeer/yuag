"""This module is the entry point for the application."""
import sys
import argparse
from sqlite3 import connect, Error, DatabaseError
from luxapp import app

DATABASE_URL = 'file:lux.sqlite?mode=ro'

def validate_port(input_port):
    """Validates the provided port number and returns its integer representation.

    Args:
        input_port (str): Input port value as a string.

    Returns:
        int: Integer representation of the port if it is a non-negative integer.

    Raises:
        ValueError: If the input_port cannot be converted to an integer or is not a positive integer.
    """
    try:
        port = int(input_port)
    except ValueError:
        raise ValueError("Port number must be an integer.")

    if not port>=0:
        raise ValueError("Port number must be above 0")

    return port


def test_database_connection():
    """Tests the database connection using the DATABASE_URL.

    Raises:
        DatabaseError: If there's a database-specific error.
        Error: For general SQLite errors.
    """
    with connect(DATABASE_URL, isolation_level=None, uri=True) as conn:
        pass  # Connection will be closed automatically after the 'with' block.

def run_app_on_port(port):
    """Starts the Flask app on the given port.

    Args:
        port (int): Port number for the Flask app to run on.
    """
    app.run(host='0.0.0.0', port=port, debug=True)

def main(port):
    """Initializes the application and starts the server.

    Args:
        port (str): Port number as a string.
    """
    try:
        port_num = validate_port(port)
    except ValueError as ve:
        print(f"Error: {ve}", file=sys.stderr)
        sys.exit(1)

    try:
        test_database_connection()
        run_app_on_port(port_num)
    except (DatabaseError, Error) as db_ex:
        print(f"Database connection error: {db_ex}", file=sys.stderr)
        sys.exit(1)
    except Exception as ex:
        print(f"An unexpected error occurred: {ex}", file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='The YUAG search application', allow_abbrev=False)
    parser.add_argument('port', help='the port at which the server should listen')
    args = parser.parse_args()
    
    # This will now handle non-integer port values gracefully
    main(args.port)

