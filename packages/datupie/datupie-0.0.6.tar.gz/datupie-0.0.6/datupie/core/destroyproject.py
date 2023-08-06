import requests
import os
import json

class DestroyCommand:
    def __init__(self):
        self.uri = "http://35.172.203.237:8081/destroy"
    
    def destroyproject(self):
        name_project = input("Type the name of (data science) project you would to destroy: ")
        data = dict({'project':name_project, 'file':name_project})
        response = requests.post(self.uri, json=data)
        print(response.text)
        