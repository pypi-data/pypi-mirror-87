"""
google.py
written in Python3
author: C. Lockhart <chris@lockhartlab.org>
"""

from iox._config import google as config

from hashlib import md5
from glovebox import GloveBox
from googleapiclient.discovery import build
from google.cloud import bigquery
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import numpy as np
import os.path
import pandas as pd
import pickle


# Allows data extract from BigQuery database
class BigQuery:
    """
    Connect to BigQuery
    """

    # Privatize class variables
    # project_id = privatize(dtype='str', immutable=True)
    # credentials = privatize(dtype='str', immutable=True)
    # client = privatize(dtype=(None, bigquery.Client))

    # Initialize the instance
    # TODO add ability to authenticate via API key
    def __init__(self, project_id=None, credentials=None):
        """
        Initialize instance of BigQuery class

        Parameters
        ----------
        project_id : str
            Google project ID
        credentials : str
            Path to Google credentials
        """

        # Get project ID from config if not specified
        if project_id is None:
            project_id = config['project_id']
            if project_id is None:
                raise AttributeError('must specify a project ID')

        # Save information
        self.project_id = project_id
        self.credentials = credentials
        self.client = None

    # Connection check
    def _connection_check(self):
        """
        Connect if the connection has not already been set up
        """

        if self.client is None:
            self.connect()

    # Connect to client
    def connect(self):
        """
        Start the client connection with BigQuery using :func:`~iox.authenticate`
        """

        # Authenticate credentials
        _credentials = authenticate('https://www.googleapis.com/auth/bigquery', self.credentials)

        # Connect to client and save
        self.client = bigquery.Client(self.project_id, _credentials)

    # TODO add create_table method
    def create_table(self, table):
        pass

    def create_view(self, view, sql):
        # Check that the connection is active
        self._connection_check()

        # Define the view
        view = bigquery.Table(view)
        view.view_query = sql

        # Create the view
        _ = self.client.create_table(view)

    # Delete table in BigQuery
    def delete_table(self, table):
        """
        Delete table in BigQuery

        Parameters
        ----------
        table : str
            Name of table to be deleted
        """

        # Check that the connection is active
        self._connection_check()

        # Delete the table
        self.client.delete_table(table, not_found_ok=True)

    # TODO execute SQL code without intention to return
    def execute(self, sql):
        pass

    # Query database with a file
    def fquery(self, filename):
        """
        Query database with a file.

        Parameters
        -------
        filename : str
            Path to file that contains a SQL query.

        Returns
        -------
        pandas.DataFrame
            The results from the query
        """

        # Open file, read in query, and run it
        with open(filename, 'r') as file_stream:
            sql = file_stream.read()
            return self.query(sql)

    # Get view query
    def get_view(self, view):
        """
        Get the query in BigQuery view

        Parameters
        ----------
        view : str
            Reference to view

        Returns
        -------
        str
            View query
        """

        # Check that the connection is active
        self._connection_check()

        # Return the view as a string
        return self.client.get_table(view).view_query

    # To CSV
    def to_csv(self, sql, filename, index=True):
        """
        Query the database and then write to CSV

        Parameters
        ----------
        sql : str
            SQL statements to be run.
        filename : str
            Name of CSV.
        index : bool
            Should index be written? (Default: True)
        """

        # Query the database
        df = self.query(sql)

        # Write to CSV
        df.to_csv(filename, index=index)

    def update_view(self, view, sql):
        # Check that the connection is active
        self._connection_check()

        # Define the view
        view = bigquery.Table(view)
        view.view_query = sql

        # Update the view
        _ = self.client.update_table(view, ["view_query"])

    # Query database with a string
    def query(self, sql, set_index=True):
        """
        Query database with a string.

        Parameters
        ----------
        sql : str
            SQL statements to be run.
        set_index : bool

        Returns
        -------
        pandas.DataFrame
            The results from the query
        """

        # Check that we are connected to BigQuery
        self._connection_check()

        # Run SQL
        df = self.client.query(sql).to_dataframe()

        # Set index?
        if set_index:
            df = df.set_index(df.columns[0])

        # Return
        return df


# Class for reading & writing to Google Sheets
class GoogleSheet:
    """
    Read and write to Google sheets.
    """

    # Initialize the class instance
    def __init__(self, spreadsheet_id, credentials=None):
        self.spreadsheet_id = spreadsheet_id
        self.credentials = credentials
        self.spreadsheet = None

    # Clear
    def _clear(self, cell):
        """
        Clear cell range.

        Parameters
        ----------
        cell : str
            Cell range to clear.
        """

        # Define parameters
        params = {
            'spreadsheetId': self.spreadsheet_id,
            'range': cell,
            'body': {}
        }

        # Clear cells
        _ = self.spreadsheet.values().clear(**params).execute()

    # Check if we're connected
    def _connection_check(self):
        """
        Connect to Google API services if not connected.
        """

        if self.spreadsheet is None:
            self.connect()

    # Retrieve the ID of a sheet in the spreadsheet
    def _get_sheet_id(self, sheet=None):
        sheets = self.spreadsheet.get(spreadsheetId=self.spreadsheet_id).execute()['sheets']
        properties = pd.DataFrame(sheets)['properties']
        _sheet_ids = pd.DataFrame(properties.tolist())
        sheet_ids = dict(zip(_sheet_ids['title'], _sheet_ids['sheetId']))
        return sheet_ids if sheet is None else sheet_ids[sheet]

    # Helper function to read
    def _read(self, cell, formula=False):
        # Define parameters
        params = {
            'spreadsheetId': self.spreadsheet_id,
            'range': cell,
        }

        # Read the sheet as text or formulas?
        if not formula:
            params['valueRenderOption'] = 'UNFORMATTED_VALUE'
            params['dateTimeRenderOption'] = 'FORMATTED_STRING'
        else:
            params['valueRenderOption'] = 'FORMULA'

        # Read using API
        result = self.spreadsheet.values().get(**params).execute()

        # Return values
        return result.get('values', [])

    # Write
    def _write(self, cell, values, formula=False):
        # Parameters
        params = {
            'spreadsheetId': self.spreadsheet_id,
            'range': cell,
            'body': {'values': values},
            'valueInputOption': 'USER_ENTERED' if formula else 'RAW',
        }

        # Execute the write
        _ = self.spreadsheet.values().update(**params).execute()

    # Add sheet
    def add_sheet(self):
        pass

    # Connect
    def connect(self):
        # Authenticate credentials
        _credentials = authenticate('https://www.googleapis.com/auth/spreadsheets', self.credentials)

        # Connect to sheet
        self.spreadsheet = build('sheets', 'v4', credentials=_credentials).spreadsheets()

    def copy_sheet(self, from_sheet, to_sheet):
        sheet_ids = self._get_sheet_id()
        from_sheet_id = sheet_ids[from_sheet]
        if to_sheet in sheet_ids:
            to_sheet_id = sheet_ids[to_sheet]
        else:
            pass

    def delete_sheet(self, sheet):
        """
        Delete sheet by name from Google spreadsheet.

        Parameters
        ----------
        sheet : str
            Name of Google sheet.
        """

        self.delete_sheet_id(self._get_sheet_id(sheet))

    def delete_sheet_id(self, sheet_id):
        """
        Delete sheet by ID from Google spreadsheet.

        Parameters
        ----------
        sheet_id : int
            ID of Google sheet, i.e., https://docs.google.com/spreadsheets/d/[spreadsheet_id]/edit#gid=[sheet_id]
        """

        parameters = {
            'requests': [
                {
                    'deleteSheet': {
                        'sheetId': sheet_id
                    }
                }
            ]
        }

        _ = self.spreadsheet.batchUpdate(spreadsheetId=self.spreadsheet_id, body=parameters).execute()

    def clear(self, cell):
        # Check that we're connected
        self._connection_check()

        # Clear
        self._clear(cell)

    def copy(self, cell1, cell2, formula=True):
        # Check that we're connected
        self._connection_check()

        # Read
        values = self._read(cell1, formula=formula)

        # Write to new range
        self._write(cell2, values, formula=formula)

    # Read
    def read(self, cell, header=False):
        """
        Read from Google sheets.

        Parameters
        ----------
        cell : str
            Location of cells to read in A4 format.
        header : bool
            Is there a header present in the range?

        Returns
        -------
        pandas.DataFrame
            Cells returned as a DataFrame.
        """

        # Check that we're connected
        self._connection_check()

        # Read
        values = self._read(cell, formula=False)

        # Convert to DataFrame
        df = pd.DataFrame(values)

        # Fix headers?
        if header:
            df = df.rename(columns=df.iloc[0]).drop(df.index[0])

        # Return
        return df

    # Write
    def write(self, cell, values, index=False, header=True, formula=False):
        """

        Parameters
        ----------
        cell : str
        values : pd.DataFrame or array-like or singular
        index
        header
        formula : bool

        Returns
        -------

        """

        # Convert DataFrame to correct format
        if isinstance(values, pd.DataFrame):
            # Include index if necessary
            if index:
                values = values.copy().reset_index()

            # Include header if necessary
            header_values = []
            if header:
                header_values = [values.columns.values.tolist()]

            # Convert into usable format
            values = header_values + values.iloc[:, :].values.tolist()

        # If list-like, convert to correct format
        elif isinstance(values, (list, tuple, np.ndarray)):
            values = [values]

        # If singular, convert
        elif isinstance(values, (int, bool, str, float)):
            values = [[values]]

        # Write
        self._write(cell, values, formula=formula)


# Authenticate:
def authenticate(endpoint, credentials=None):
    """
    Authenticate Google

    Parameters
    ----------
    endpoint : str
        Google scope to authenticate
    credentials : None or str
        Google credentials

    Returns
    -------
    google.oauth2.credentials.Credentials
        Authenticated credentials
    """

    # Get credentials from configuration if not set
    if credentials is None:
        credentials = config['credentials']

    # Type check
    if not isinstance(endpoint, str):
        raise AttributeError('endpoint must be a string')
    if not isinstance(credentials, str):
        raise AttributeError('credentials must be a string')

    # Check if credentials.json exists
    if not os.path.isfile(credentials):
        raise AttributeError("""
            %s does not exist
            you can create it at 
            https://cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries
        """ % credentials)

    # Name our authentication token and place it in tempdir
    token_name = os.path.join(GloveBox('iox-google', persist=True).path, md5(endpoint.encode()).hexdigest() + '.pickle')

    # Dummy for authenticated credentials
    _credentials = None

    # If the token already exists, read in
    if os.path.exists(token_name):
        with open(token_name, 'rb') as token_stream:
            _credentials = pickle.load(token_stream)

    # If there are no valid credentials, generate
    if not _credentials or not _credentials.valid:
        # Simply refresh if possible
        if _credentials and _credentials.expired and _credentials.refresh_token:
            _credentials.refresh(Request())

        # Otherwise, generate
        else:
            # BUGFIX: #1 (https://github.com/LockhartLab/izzy/issues/1)
            flow = InstalledAppFlow.from_client_secrets_file(credentials, [endpoint])
            _credentials = flow.run_local_server()

        # Save the new authenticated credentials
        with open(token_name, 'wb') as token_stream:
            pickle.dump(_credentials, token_stream)

    # Return the authenticated credentials
    return _credentials


# Clean stored credentials
def clean_stored_credentials():
    GloveBox('iox-google').delete()


# TODO create credentials
def create_credentials():
    pass
