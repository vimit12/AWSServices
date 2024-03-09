"""
    File: json_validator.py
    Author: Vimit
"""

__author__ = "Vimit"
__version__ = "0.1.0"

import json
import os

import jsonschema

current_path = os.path.abspath(__file__)
current_directory = os.path.dirname(current_path)


class CustomJsonValidator:
    """
    A class to validate JSON data against a JSON schema.

    Parameters:
        filename (str): The name of the JSON schema file to validate against.
        request_body_data (dict): The JSON data to be validated.

    Returns:
        bool: True if the JSON data is valid against the schema, False otherwise.
    """

    def __init__(self, filename, request_body_data, app_name):
        """
        Constructor method for CustomJsonValidator.

        Loads the JSON schema from the file specified by `filename`, and validates the `request_body_data`
        against the schema.

        Parameters:
            filename (str): The name of the JSON schema file to validate against.
            request_body_data (dict): The JSON data to be validated.
        """
        self.app_name = app_name
        self.filename = filename
        self.request_body_data = request_body_data
        self.flag = False
        self.message = None
        # validate json
        self._validate_schema()

    def _load_schema(self):
        """
        Load the JSON schema from the specified file.

        Returns:
            dict: The loaded JSON schema.
        """
        with open(
            f"{current_directory}/schemas/{self.app_name}/{self.filename}", "r"
        ) as schema:
            schema_data = json.load(schema)
        return schema_data

    def _validate_schema(self):
        """
        Validates the JSON data against the JSON schema.

        Returns:
            bool: True if the JSON data is valid against the schema, False otherwise.
        """
        schema = self._load_schema()
        try:
            jsonschema.validate(instance=self.request_body_data, schema=schema)
            print("JSON is valid according to schema")
            self.flag = True
        except jsonschema.exceptions.ValidationError as err:
            print(f"Validation error: {err.message}")
            self.message = err.message
