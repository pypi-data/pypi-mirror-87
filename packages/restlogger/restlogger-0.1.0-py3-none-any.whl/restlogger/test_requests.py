import unittest
from .class_requests import Request_Class

class Requests_Test(unittest.TestCase):

    def test_set_request(self):
        test_url = 'http://api.openweathermap.org/data/2.5/weather?q=Zurich,CHZH&appid=3836093dde650898eb014e6f27304646'
        r = Request_Class(test_url)
        return_dict = r.set_request()
        self.assertEqual(return_dict, 'Zurich')

    def test_parse_json(self):
        pass

