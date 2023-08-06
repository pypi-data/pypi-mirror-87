import requests
import json

class Request_Class():
    def __init__(self, url_address):
        self.url_address = url_address

    def set_request(self):
        req_data = requests.get(self.url_address)

        r_dict = req_data.json()
        print('---------------------------')
        print(type(r_dict))
        print("---------------------------")

        return r_dict

    def parse_json(self, dict):
        print('--------test2--------')
        print(type(dict))
        


