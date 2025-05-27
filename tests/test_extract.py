import unittest
from unittest.mock import patch, MagicMock
from utils.extract import scrape_fashion_studio, extract_product_info, scrape_page_content
from bs4 import BeautifulSoup
import requests


class TestScrapeFashionStudio(unittest.TestCase):

    @patch('utils.extract.requests.Session.get')
    def test_scrape_fashion_studio_returns_data(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.content = b"""
        <html>
            <body>
                <div class="collection-card">
                    <h3 class="product-title">Vintage Shirt</h3>
                    <p class="price">Rp35.000</p>
                    <p style="font-size: small">Rating: 4.2</p>
                    <p style="font-size: small">Colors: Blue, Green</p>
                    <p style="font-size: small">Size: L</p>
                    <p style="font-size: small">Gender: Male</p>
                </div>
            </body>
        </html>
        """
        mock_get.return_value = mock_response

        result = scrape_fashion_studio("https://fashion-studio.dicoding.dev/", max_pages=1)

        self.assertIsInstance(result, list)
        self.assertGreater(len(result), 0)
        self.assertEqual(result[0]["Title"], "Vintage Shirt")
        self.assertEqual(result[0]["Price"], "Rp35.000")
        self.assertIn("Blue", result[0]["Colors"])
        self.assertEqual(result[0]["Size"], "L")
        self.assertEqual(result[0]["Gender"], "Male")
        self.assertEqual(result[0]["Rating"], "4.2")

    def test_extract_product_info_missing_fields(self):
        html = "<div class='collection-card'><p>Missing info</p></div>"
        soup = BeautifulSoup(html, "html.parser")
        card = soup.find("div", class_="collection-card")
        result = extract_product_info(card)
        self.assertEqual(result["Title"], "Title Not Found")
        self.assertEqual(result["Price"], "Price Not Found")

    @patch('utils.extract.requests.Session.get')
    def test_scrape_empty_page(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.content = b"<html><body><p>No products here</p></body></html>"
        mock_get.return_value = mock_response

        result = scrape_fashion_studio("https://dummy-url.com", max_pages=1)
        self.assertEqual(result, [])

    @patch('utils.extract.requests.Session.get')
    def test_scrape_page_no_next_button(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.content = b"""
        <html>
            <body>
                <div class="collection-card">
                    <h3 class="product-title">Item</h3>
                    <span class="price">$10</span>
                </div>
            </body>
        </html>
        """
        mock_get.return_value = mock_response

        result = scrape_fashion_studio("https://dummy-url.com", max_pages=1)
        self.assertEqual(len(result), 1)

    @patch('utils.extract.requests.Session.get')
    def test_scrape_page_content_error(self, mock_get):
        mock_get.side_effect = requests.exceptions.RequestException("Network error")

        result = scrape_page_content("https://dummy-url.com")
        self.assertIsNone(result)

    def test_extract_product_info_exception(self):
        class BrokenCard:
            def find(self, *args, **kwargs):
                raise Exception("Parsing error")
            def find_all(self, *args, **kwargs):
                raise Exception("Parsing error")
        result = extract_product_info(BrokenCard())
        self.assertEqual(result["Title"], "Error")
        self.assertEqual(result["Price"], "Error")

    @patch('utils.extract.scrape_page_content')
    def test_scrape_fashion_studio_general_exception(self, mock_scrape):
        mock_scrape.side_effect = Exception("Unexpected error")
        result = scrape_fashion_studio("https://dummy-url.com", max_pages=1)
        self.assertEqual(result, [])


if __name__ == '__main__':
    unittest.main()
