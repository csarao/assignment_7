"""Handles reading and parsing transaction input data from CSV or JSON files."""

import csv
import json
from os import path

__author__ = "Chatterdeep Singh Sarao"
__version__ = "1.0.0"
__credits__ = "COMP-1327 Faculty"

class InputHandler:
    """
     A class to handle reading input transaction data from various file formats.

    This class supports reading from CSV and JSON files. It detects the file
    format based on the file extension and parses the data accordingly into a
    list of transaction records (dictionaries).
    
    """

    def __init__(self, file_path: str):
        """Initializes the InputHandler with the path to the input file.

        Parameters:
            file_path (str): The path to the transaction data file."""

        self.__file_path = file_path

    @property
    def file_path(self) -> str:
        """Returns the path of the input file.

        Returns:
            str: The full file path provided at initialization."""

        return self.__file_path

    def get_file_format(self) -> str:
        """
        Determines the file format based on the file extension.

        Returns:
            str: The file format (e.g., 'csv' or 'json').
        """
        return self.__file_path.split(".")[-1]

    def read_input_data(self) -> list:
        """
        Reads transaction data from the input file and returns it as a list.

        Automatically determines whether the file is in CSV or JSON format
        and calls the appropriate parser.

        Returns:
            list: A list of transaction records as dictionaries.

        Raises:
            FileNotFoundError: If the specified file does not exist."""

        transactions = []
        file_format = self.get_file_format()
        
        if file_format == "csv":
            transactions =  self.read_csv_data()
        elif file_format == "json":
            transactions = self.read_json_data()

        return transactions

    def read_csv_data(self) -> list:
        """
        Reads transaction data from a CSV file.

        Returns:
            list: A list of transaction records as dictionaries.

        Raises:
            FileNotFoundError: If the CSV file does not exist."""

        if not path.isfile(self.__file_path):
            raise FileNotFoundError(f"File: {self.__file_path} does not exist.")

        transactions = []

        with open(self.__file_path, "r") as input_file:
            reader = csv.DictReader(input_file)
            for row in reader:
                transactions.append(row)
            
        return transactions
            
    def read_json_data(self) -> list:
        """ Reads transaction data from a JSON file.

        Returns:
            list: A list of transaction records as dictionaries.

        Raises:
            FileNotFoundError: If the JSON file does not exist."""

        # Research the json.load function so that you 
        # understand the format of the data once it is
        # placed into input_data
        if not path.isfile(self.__file_path):
            raise FileNotFoundError(f"File: {self.__file_path} does not exist.")

        with open(self.__file_path, "r") as input_file:
            transactions = json.load(input_file)

        return transactions
    
    def data_validation(self, transactions: list) -> list:
        """
        Validates a list of transaction records.

        This method checks each transaction to ensure the 'Amount' is a non-negative
        numeric value and the 'Transaction type' is one of the accepted types:
        'deposit', 'withdrawal', or 'transfer'. Only valid transactions are returned.

        Parameters:
            transactions (list): A list of dictionaries containing transaction data.

        Returns:
            list: A list of dictionaries containing only valid transactions.

        Raises:
            KeyError: If required keys are missing in any transaction.
        
        References:
            - Python type checking and exception handling concepts from Assignments 4–6.
            - Stack Overflow discussion on safe float conversion and validation:
              https://stackoverflow.com/questions/209513/convert-string-to-float-or-int
        """
        valid_transactions = []
        valid_types = {'deposit', 'withdrawal', 'transfer'}

        for transaction in transactions:
            try:
                amount = float(transaction.get("Amount", -1))
                transaction_type = transaction.get("Transaction type", "").lower()

                if amount >= 0 and transaction_type in valid_types:
                    valid_transactions.append(transaction)

            except (ValueError, TypeError):
                continue  # Skip transactions with invalid amount
        return valid_transactions
