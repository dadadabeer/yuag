"""
Flask app for the LUX project.
"""
import json
from flask import Flask, request, make_response, render_template, abort
from luxdetails import format_entry_results2
from ps1lux import search

#-----------------------------------------------------------------------

app = Flask(__name__)

#-----------------------------------------------------------------------

@app.route('/', methods=['GET'])
@app.route('/index', methods=['GET'])
def index():
    # Attempt to load the search parameters from cookies
    search_parameters = request.cookies.get('search_parameters')
    prev_label, prev_classifier, prev_agent, prev_date = '', '', '', ''
    objects = None
    error_message = ''

    if search_parameters:
        search_parameters = json.loads(search_parameters)
        prev_label = search_parameters.get('label', '')
        prev_classifier = search_parameters.get('classifier', '')
        prev_agent = search_parameters.get('agent', '')
        prev_date = search_parameters.get('date', '')

        # Perform the search to populate the results
        objects = search(prev_label, prev_classifier, prev_agent, prev_date)
        if not objects:
            # If no objects were found and search was attempted, set an error message
            error_message = "No results found for the last search."

    # Pass the objects and error_message to the template
    html = render_template('index.html', label=prev_label,
                           classifier=prev_classifier,
                           agent=prev_agent,
                           date=prev_date,
                           objects=objects,
                           error_message=error_message)
    response = make_response(html)
    return response


#-----------------------------------------------------------------------

@app.route('/search', methods=['GET'])
def search_results():
    # Retrieve search parameters from the request, defaulting to an empty string
    label = request.args.get('l', default='')
    classifier = request.args.get('c', default='')
    agent = request.args.get('a', default='')
    date = request.args.get('d', default='')

    # Perform the search with the provided parameters
    objects = search(label, classifier, agent, date)

    # If no search parameters were provided and no previous search, show a default message or empty results
    if not (label or classifier or agent or date) and not request.cookies.get('search_parameters'):
        error_message = "No search terms provided. Please enter some search terms."
        html = render_template('search_results.html', error_message=error_message)
    else:
        # Render the search results with the objects found
        html = render_template('search_results.html', objects=objects)

    # Create a response object with the rendered HTML
    response = make_response(html)

    # Store search parameters in a cookie as a JSON string
    search_params = {'label': label, 'classifier': classifier, 'agent': agent, 'date': date}
    response.set_cookie('search_parameters', json.dumps(search_params))

    return response

@app.route('/obj/<obj_id>', methods=['GET'])
def get_object_deets(obj_id):
    """
    Fetches and renders details for a specific object based on its id.

    :param obj_id: The unique id of the object to fetch details for.
    :return: The rendered details of the object or a 404 error if the object doesn't exist.
    """
    obj = format_entry_results2(obj_id)
    if obj is None:
        abort(404, description=f"Error: object with id {obj_id} does not exist")

    html = render_template('object_deets.html', obj=obj, obj_id=obj_id)
    response = make_response(html)
    response.set_cookie("activate", "true")
    return response

@app.route('/obj', methods=['GET'])
def handle_missing_obj_id():
    """
    Handles requests with missing object ids by aborting with a 404 error.

    :return: A 404 error with the description "Error: missing object ID".
    """
    abort(404, description="Error: missing object ID")

@app.errorhandler(404)
def not_found_error(error):
    """
    Handles 404 errors by rendering an error template with the appropriate error message.

    :param error: The error description.
    :return: The rendered error template with a status code of 404.
    """
    return render_template('error.html', error_message=error.description), 404
