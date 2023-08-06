from datupie.core.templates import datupie_template
#from core.templates import datupie_template
import json
import os
import re
import requests
import sys

class StartCommand:
    def __init__(self):
        self.uri = "http://35.172.203.237:8081/create"

    def startproject(self):
        new_project = input("Is this a new datup (data science) project [y/N]: ")
        if new_project == "y" or new_project == "yes" or new_project == "Y" :
            print("Choose the name of your project using lowercase names")
            print("this client will be append to your project name a <datup> prefix for IaC repository")
            print("this client will be append to your project name a <_datup> suffix for all services you need with the name of service you use")
            print("for example: <your-project-name><-datalake><-datup>")
            print("this is the simplest way to prevent errors with cloud providers services name")
            project_name = str(input("Which would be the name of project: ")).lower()
            if self.validated(project_name = project_name):
                data = self.parse_file(project_name)
                response = requests.post(self.uri, json=data)
                if response.text == "Succesfull created":
                    self.startproject()
                elif response.text == "This architecture is deployed, if you want update it invoke the right method":
                    print(response.text)
                else : print(response.text)
            else: 
                print("Something is wrong with the name you are choosing, please try again")
        elif new_project == "N" :
            print("Not configured yet")
            sys.exit(0)
        else : 
            print("Not valid")
            sys.exit(0)
    
    def validated(self, **kwards):        
        regex = re.compile("[@_!#$%^&*()<>?/\|}{~:]")
        if (regex.search(kwards["project_name"])) == None : return True
        else : return False

    def parse_file(self, project_name):        
        data = datupie_template.data()
        data["project"] = project_name
        data["file"] = project_name
        data["architecture"]["resource"]["aws_ecr_repository"]["ecr_repository"]["name"] = f"{project_name}-ecr-datup"
        data["architecture"]["resource"]["aws_codebuild_project"]["codebuild_project"]["name"] = f"{project_name}-codebuild-datup"
        data["architecture"]["resource"]["aws_s3_bucket"]["project-datalake"]["bucket"] = f"{project_name}-datalake-datup"
        data["architecture"]["resource"]["aws_codecommit_repository"]["project-repository"]["repository_name"] = f"{project_name}-datup"
        data["architecture"]["resource"]["aws_s3_bucket_object"]["dev_enviroment"]["bucket"] = f"{project_name}-datalake-datup"
        data["architecture"]["resource"]["aws_s3_bucket_object"]["prod_enviroment"]["bucket"] = f"{project_name}-datalake-datup"
        
        return data

     

        