"""
Object class for Yale University Art Gallery Item.
"""

import requests

class Object:
    def __init__(self, obj_id=None, acc_no=None, date=None, place=None, dept=None, label=None,
                 agents=None, classifiers=None, productions=None, references=None):
        self._id = obj_id
        self._acc_no = acc_no
        self._date = date
        self._place = place
        self._dept = dept
        self._label = label
        self._image_exists = False  # Initialize the flag as False

        # Construct URL only if obj_id is not None
        if obj_id:
            url = f"https://media.collections.yale.edu/thumbnail/yuag/obj/{obj_id}"
            response = requests.get(url, allow_redirects=True)
            if response.status_code == 200:
                self._url = url
                self._image_exists = True  # Set the flag to True if the image exists
            else:
                self._url = None

        self._agents = agents or []
        self._classifiers = classifiers or []
        self._productions = productions or []
        self._references = references or []

    def has_image(self):
        """
        Determines if the object has an associated image URL that exists.

        Returns:
            bool: True if the object has a valid obj_id and the image exists, otherwise False.
        """
        return self._image_exists


    def get_id(self):
        """Returns the unique identifier of the object."""
        return self._id

    def get_acc_no(self):
        """Returns the accession number of the object."""
        return self._acc_no

    def get_date(self):
        """Returns the date associated with the object."""
        return self._date

    def get_place(self):
        """Returns the place associated with the object."""
        return self._place

    def get_dept(self):
        """Returns the department associated with the object."""
        return self._dept

    def get_label(self):
        """Returns the label of the object."""
        return self._label

    def get_agents(self):
        """Returns the list of agents associated with the object."""
        return self._agents

    def get_classifiers(self):
        """Returns the list of classifiers associated with the object."""
        return self._classifiers

    def get_productions(self):
        """Returns the list of productions associated with the object."""
        return self._productions

    def get_references(self):
        """Returns the list of references associated with the object."""
        return self._references
