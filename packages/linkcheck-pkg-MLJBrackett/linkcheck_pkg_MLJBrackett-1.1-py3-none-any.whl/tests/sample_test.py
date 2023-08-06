import unittest
from link_check import requestUrl, checkUrl, parser, singleUrlCheck
from unittest.mock import patch


class TestResponseOutput(unittest.TestCase):
    @patch("link_check.requests.head")  # Mock 'requests' module 'get' method.
    def test_url_good(self, mock_head):
        singleUrlGood = ["https://mljbrackett.com"]
        mock_head.return_value.status_code = 200
        for url in singleUrlGood:
            response = requestUrl(url)
        self.assertEqual(
            checkUrl(response, singleUrlGood),
            "GOOD",
            "Should be 'GOOD'",
        )

    @patch("link_check.requests.head")  # Mock 'requests' module 'get' method.
    def test_url_error(self, mock_head):
        singleUrlError = ["https://mljbrackett.com/notarealroute"]
        mock_head.return_value.status_code = 404
        for url in singleUrlError:
            response = requestUrl(url)
        self.assertEqual(
            checkUrl(response, singleUrlError),
            "CLIENT/SERVER ISSUE",
            "Should be 'CLIENT/SERVER ISSUE'",
        )

    @patch("link_check.requests.head")  # Mock 'requests' module 'get' method.
    def test_url_redirect(self, mock_head):
        singleUrlRedirect = ["http://mljbrackett.com"]
        mock_head.return_value.status_code = 300
        for url in singleUrlRedirect:
            response = requestUrl(url)
        self.assertEqual(
            checkUrl(response, singleUrlRedirect),
            "REDIRECT",
            "Should be 'REDIRECT'",
        )


class TestURLOutput(unittest.TestCase):
    @patch("link_check.requests.head")  # Mock 'requests' module 'get' method.
    def test_url_good(self, mock_head):
        singleUrlGood = ["https://mljbrackett.com"]
        mock_head.return_value.status_code = 200
        for url in singleUrlGood:
            response = requestUrl(url)
        self.assertEqual(
            singleUrlCheck(response, singleUrlGood),
            "GOOD",
            "Should be 'GOOD'",
        )

    @patch("link_check.requests.head")  # Mock 'requests' module 'get' method.
    def test_url_error(self, mock_head):
        singleUrlError = ["https://mljbrackett.com/notarealroute"]
        mock_head.return_value.status_code = 404
        for url in singleUrlError:
            response = requestUrl(url)
        self.assertEqual(
            singleUrlCheck(response, singleUrlError),
            "CLIENT/SERVER ISSUE",
            "Should be 'CLIENT/SERVER ISSUE'",
        )

    @patch("link_check.requests.head")  # Mock 'requests' module 'get' method.
    def test_url_redirect(self, mock_head):
        singleUrlRedirect = ["http://mljbrackett.com"]
        mock_head.return_value.status_code = 300
        for url in singleUrlRedirect:
            response = requestUrl(url)
        self.assertEqual(
            singleUrlCheck(response, singleUrlRedirect),
            "REDIRECT",
            "Should be 'REDIRECT'",
        )


class TestUrlResponse(unittest.TestCase):
    @patch("link_check.requests.head")  # Mock 'requests' module 'get' method.
    def test_url_request_200(self, mock_head):
        singleUrl200 = ["https://mljbrackett.com"]
        mock_head.return_value.status_code = 200
        response = requestUrl(singleUrl200)
        self.assertEqual(response, 200, "Should be 200")

    @patch("link_check.requests.head")  # Mock 'requests' module 'get' method.
    def test_url_request_300(self, mock_head):
        singleUrl300 = ["http://mljbrackett.com"]
        mock_head.return_value.status_code = 300
        response = requestUrl(singleUrl300)
        self.assertEqual(response, 300, "Should be 300")

    @patch("link_check.requests.head")  # Mock 'requests' module 'get' method.
    def test_url_request_400(self, mock_head):
        singleUrl400 = ["https://mljbrackett.com/notarealroute"]
        mock_head.return_value.status_code = 400
        response = requestUrl(singleUrl400)
        self.assertEqual(response, 400, "Should be 400")

    def test_url_request_timeout(self):
        singleUrlTimeout = ["https://mljbrackett.co"]
        self.assertEqual(
            requestUrl(singleUrlTimeout),
            "TIMEOUT",
            "Should be 'TIMEOUT'",
        )

    def test_url_request_no_array(self):
        singleUrlTimeout = [""]
        self.assertEqual(
            requestUrl(singleUrlTimeout),
            "TIMEOUT",
            "Should be 'TIMEOUT'",
        )


class TestParser(unittest.TestCase):
    def testArgs(self):
        parserTest = str(parser.parse_args())
        self.assertEqual(
            parserTest,
            "Namespace(bad=None, file=None, good=None, ignore=None, json=None, redirect=None, telescope=None, url=None, version=False)",
            "Should be 'Namespace(bad=None, file=None, good=None, ignore=None, json=None, redirect=None, telescope=None, url=None, version=False)', if you have added more args, add tests for them! (And update this test)",
        )


if __name__ == "__main__":
    unittest.main()
