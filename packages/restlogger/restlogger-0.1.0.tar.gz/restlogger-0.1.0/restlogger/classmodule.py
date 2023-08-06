import logging
import csv
import io

class My_Class():
    def __init__(self, name):
        self.name = name

    def say_name(self):
        print('name is {}'.format(self.name))


