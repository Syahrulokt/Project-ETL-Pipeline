import unittest
from unittest.mock import patch, MagicMock
import pandas as pd
from utils import load

class TestLoadFunctions(unittest.TestCase):

    @patch('utils.load.pd.DataFrame.to_csv')
    @patch('utils.load.os.makedirs')
    def test_save_to_csv(self, mock_makedirs, mock_to_csv):
        df = pd.DataFrame({
            'title': ['Kemeja', 'Sweater'],
            'price': [20000, 40000],
            'rating': [4.1, 4.6]
        })

        result = load.save_to_csv(df, 'dummy/products.csv')

        mock_makedirs.assert_called_once()
        mock_to_csv.assert_called_once_with('dummy/products.csv', index=False)
        self.assertTrue(result)

    @patch('utils.load.build')
    @patch('utils.load.Credentials.from_service_account_file')
    @patch('utils.load.os.path.exists', return_value=True)
    def test_load_to_gsheet(self, mock_exists, mock_creds_loader, mock_build):
        df = pd.DataFrame({
            'title': ['Rok', 'Blazer'],
            'price': [55000, 75000],
            'rating': [4.3, 4.9]
        })

        mock_creds_loader.return_value = MagicMock()
        mock_service = MagicMock()
        mock_build.return_value = mock_service
        mock_service.spreadsheets.return_value.values.return_value.update.return_value.execute.return_value = {'updatedCells': 6}

        result = load.load_to_gsheet(df, 'dummy_spreadsheet_id', 'Sheet1!A1')

        self.assertTrue(result)
        mock_build.assert_called_once()
        mock_creds_loader.assert_called_once()
        mock_service.spreadsheets.return_value.values.return_value.update.assert_called_once()
        mock_service.spreadsheets.return_value.values.return_value.update.return_value.execute.assert_called_once()

if __name__ == '__main__':
    unittest.main()
