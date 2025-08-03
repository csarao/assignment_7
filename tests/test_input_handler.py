"""UNIT TESTING"""

import unittest
from unittest import TestCase
from unittest.mock import patch, mock_open
from input_handler.input_handler import InputHandler

__author__ = "Chatterdeep Singh"
__version__ = "1.0.0"
__credits__ = "COMP-1327 Faculty"


class InputHandlerTests(TestCase):
    """Defines the unit tests for the InputHandler class."""

    def setUp(self):
        """Sets up reusable CSV test content."""
        self.FILE_CONTENTS = (
            "Transaction ID,Account number,Date,Transaction type,"
            "Amount,Currency,Description\n"
            "1,1001,2023-03-01,deposit,1000,CAD,Salary\n"
            "2,1002,2023-03-01,deposit,1500,CAD,Salary\n"
            "3,1001,2023-03-02,withdrawal,200,CAD,Groceries"
        )

    def test_get_file_format_returns_csv(self):
        """Test that get_file_format returns correct file extension."""
        handler = InputHandler("data/sample.csv")
        self.assertEqual(handler.get_file_format(), "csv")

    def test_read_csv_data_file_not_found(self):
        """Test that FileNotFoundError is raised for non-existent CSV file."""
        handler = InputHandler("missing.csv")
        with self.assertRaises(FileNotFoundError):
            handler.read_csv_data()

    @patch("os.path.isfile", return_value=True)
    def test_read_csv_data_returns_list(self, mock_exists):
        """Test that read_csv_data returns a list from valid CSV data."""
        handler = InputHandler("transactions.csv")
        m = mock_open(read_data=self.FILE_CONTENTS)

        with patch("builtins.open", m):
            result = handler.read_csv_data()

        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 3)

    @patch("os.path.isfile", return_value=True)
    def test_read_input_data_returns_csv_list(self, mock_exists):
        """Test that read_input_data returns list for CSV input."""
        handler = InputHandler("transactions.csv")
        m = mock_open(read_data=self.FILE_CONTENTS)

        with patch("builtins.open", m):
            result = handler.read_input_data()

        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 3)

    @patch("builtins.open", new_callable=mock_open, read_data='[{"id":1},{"id":2}]')
    @patch("os.path.isfile", return_value=True)
    def test_read_input_data_returns_json_list(self, mock_exists, mock_file):
        """Test that read_input_data returns list for JSON input."""
        handler = InputHandler("transactions.json")
        result = handler.read_input_data()
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 2)

    def test_read_input_data_returns_empty_list_for_unknown_format(self):
        """Test that read_input_data returns empty list for unknown format."""
        handler = InputHandler("transactions.txt")
        result = handler.read_input_data()
        self.assertEqual(result, [])


if __name__ == "__main__":
    unittest.main()