import unittest
import pandas as pd
import numpy as np
from utils import transform  # Sesuaikan dengan struktur foldermu

class TestTransform(unittest.TestCase):

    def test_format_price_with_dollar_and_exchange(self):
        # Data dummy dengan format dollar
        products = [
            {
                'Title': 'Product A',
                'Price': '$15.00',
                'Rating': 'Rated 4.2 out of 5',
                'Colors': 'Available in 2 colors',
                'Size': 'Size: XL',
                'Gender': 'Gender: Men',
                'Timestamp': '2025-05-15'
            },
            {
                'Title': 'Product B',
                'Price': '$25.50',
                'Rating': 'Rated 4.8 out of 5',
                'Colors': 'Available in 3 colors',
                'Size': 'Size: L',
                'Gender': 'Gender: Women',
                'Timestamp': '2025-05-15'
            }
        ]
        product_df = transform.transform_to_DataFrame(products)
        result_df = transform.transform_data(product_df, exchange_rate=16000)

        # Assert
        self.assertEqual(len(result_df), 2)
        self.assertIn('Price', result_df.columns)
        self.assertAlmostEqual(result_df['Price'].iloc[0], 15.00 * 16000, places=2)
        self.assertEqual(result_df['Title'].iloc[0], 'Product A')
        self.assertIsInstance(result_df['Price'].iloc[0], float)
        self.assertIn('Timestamp', result_df.columns)

    def test_invalid_price_should_be_removed(self):
        # Data dengan harga tidak valid
        products = [
            {
                'Title': 'Invalid Product',
                'Price': 'Price Not Found',
                'Rating': '4.0',
                'Colors': '1',
                'Size': 'Size: M',
                'Gender': 'Gender: Unisex',
                'Timestamp': '2024-01-01'
            }
        ]

        product_df = transform.transform_to_DataFrame(products)
        result_df = transform.transform_data(product_df)

        # Assert bahwa data dengan harga tidak valid dibuang
        self.assertEqual(len(result_df), 0)

if __name__ == '__main__':
    unittest.main()
