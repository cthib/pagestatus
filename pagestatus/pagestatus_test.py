import unittest

from pagestatus import PageStatus


class TestURLStatus(unittest.TestCase):
    
    def test_200(self):
        ps = PageStatus(url_fn="_json/test.json", log_fn="_logs/test.log")
        self.assertTrue(ps.url_status("https://httpstat.us/200"))
    
    def test_403(self):
        ps = PageStatus(url_fn="_json/test.json", log_fn="_logs/test.log")
        self.assertFalse(ps.url_status("https://httpstat.us/403"))

    def test_404(self):
        ps = PageStatus(url_fn="_json/test.json", log_fn="_logs/test.log")
        self.assertFalse(ps.url_status("https://httpstat.us/404"))

    def test_500(self):
        ps = PageStatus(url_fn="_json/test.json", log_fn="_logs/test.log")
        self.assertFalse(ps.url_status("https://httpstat.us/500"))

    def test_url_error(self):
        ps = PageStatus(url_fn="_json/test.json", log_fn="_logs/test.log")
        self.assertFalse(ps.url_status("http://somewr.ongurl"))
    

class TestPageStatus(unittest.TestCase):

    def test_update_http_count(self):
        ps = PageStatus(url_fn="_json/test.json", log_fn="_logs/test.log")
        http_200_count = ps.http_count.get(200, 0)
        ps.update_http_count(200)
        self.assertEqual(http_200_count+1, ps.http_count[200])

    def test_update_url_check_count(self):
        ps = PageStatus(url_fn="_json/test.json", log_fn="_logs/test.log")
        url_check_count = ps.url_check_count
        ps.update_url_check_count()
        self.assertEqual(url_check_count+1, ps.url_check_count)


if __name__ == '__main__':
    unittest.main()