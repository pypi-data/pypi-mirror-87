from datupie.core.startproject import StartCommand
#from core.startproject import StartCommand
import requests
import os
import json
import yaml

class DeployCommand(StartCommand):
    def __init__(self):
        StartCommand.__init__(self)
        self.uri = "http://35.172.203.237:8081/deploy"
        self.uri_status = "http://35.172.203.237:8081/status"
    
    def deployproject(self):
        
        name_project = input("Type the name of (data science) project you would to deploy: ")
        data = dict({'project':name_project, 'file':name_project})
        response = requests.post(self.uri, json=data)

        if response.text == "It seems that is already a architecture deployed":
            self.create_folder_projects(data, project_name = name_project)
        elif response.text == "Resources were not deployed":
            print("Some error ocurrs while deploying")
        else : print(response.text)

    def create_folder_projects(self,data, **kwards):
        create = str(input("Would you want to create a local project? [y/N]: "))
        uri = None
        if create == "y":
            uri = str(input("Please enter de uri where you want to save the project in your local machine, ommit the last '/': "))        
            uri = uri.replace("\\","/")

            if os.path.exists(f"{uri}/{kwards['project_name']}"):
                print("The project exists in local")
            else:
                response_status = requests.post(self.uri_status,json=data)
                status = response_status.json()
                for resource in status["values"]["root_module"]["resources"]:
                    if resource["address"] == "aws_codecommit_repository.project-repository":
                        clone_url_http = resource["values"]["clone_url_http"]
                        break
                os.system(f"git clone {clone_url_http} {uri}/{kwards['project_name']}")

                main_dirs = [kwards['project_name'],"test"]
                secondary_dirs = ["clean","prepare","transform","inference","data","train"]
                for _dir in main_dirs:
                    os.mkdir(f"{uri}/{kwards['project_name']}/{_dir}")
                    with open(f"{uri}/{kwards['project_name']}/{_dir}/routes.py","w") as route_file : 
                        route_file.write(f"import os\n\n")
                        route_file.write(f"os.environ['DEVELOPMENT_ROUTES'] = 'dev/<your dev branch>'\n")
                        route_file.write(f"os.environ['PRODUCTION_ROUTES'] = 'prod/master'\n")
                    if _dir == kwards['project_name']:
                        with open(f"{uri}/{kwards['project_name']}/{_dir}/training.py","w") as main_file : 
                            main_file.write(f"import routes\n")
                            main_file.write(f"from clean import clean\n")
                            main_file.write(f"from prepare import prepare\n")
                            main_file.write(f"from transform import transform\n")
                            main_file.write(f"from train import train\n\n")
                            main_file.write(f"if __name__ == '__main__':\n")                            
                            main_file.write(f"\t''' your code here datupian '''\n")
                            main_file.write(f"ROUTE = routes.os.environ.get('')")
                            main_file.write(f"\tpass\n")
                        with open(f"{uri}/{kwards['project_name']}/{_dir}/predicting.py","w") as main_file : 
                            main_file.write(f"import routes\n")
                            main_file.write(f"from inference import inference\n\n")
                            main_file.write(f"if __name__ == '__main__':\n")
                            main_file.write(f"\t''' your code here datupian '''\n")
                            main_file.write(f"ROUTE = routes.os.environ.get('')")
                            main_file.write(f"\tpass\n")

                for _dir in secondary_dirs:
                    os.mkdir(f"{uri}/{kwards['project_name']}/{kwards['project_name']}/{_dir}")
                    if _dir == "data" : pass
                    else :
                        with open(f"{uri}/{kwards['project_name']}/{kwards['project_name']}/{_dir}/__init__.py","w") as init_file :
                            init_file.write(f"from {_dir} import {_dir}")
                        with open(f"{uri}/{kwards['project_name']}/{kwards['project_name']}/{_dir}/{_dir}.py","w") as main_file : 
                            main_file.write(f"import datup as dt\n\n")
                            main_file.write(f"def {_dir}():\n")
                            main_file.write(f"\tpass\n")
                            main_file.write(f"\t''' your code here datupian '''")
                        with open(f"{uri}/{kwards['project_name']}/{kwards['project_name']}/{_dir}/{_dir}.ipynb","w") as _file : 
                            json.dump({
                                "metadata": {
                                    "language_info": {
                                        "codemirror_mode": {
                                            "name": "ipython",
                                            "version": 3
                                        },
                                        "file_extension": ".py",
                                        "mimetype": "text/x-python",
                                        "name": "python",
                                        "nbconvert_exporter": "python",
                                        "pygments_lexer": "ipython3",
                                        "version": 3
                                    },
                                    "orig_nbformat": 2
                                },
                                "nbformat": 4,
                                "nbformat_minor": 2,
                                "cells": [{
                                    "cell_type": "code",
                                    "execution_count": "",
                                    "metadata": {},
                                    "outputs": [],
                                    "source": [
                                        "import datup as dt\n",
                                        "import pandas as pd\n",
                                        "import numpy as np"
                                    ]
                                }]
                            }, _file)

        response_status = requests.post(self.uri_status,json=data)
        if os.path.exists(f"{uri}/{kwards['project_name']}"):
            with open(f"{uri}/{kwards['project_name']}/{kwards['project_name']}.tf.json", "w") as _file:
                json.dump(response_status.json(),_file)
            with open(f"{uri}/{kwards['project_name']}/project.json", "w") as _file:
                json.dump({
                    "metadata":{
                        "project" : f"{kwards['project_name']}",
                        "architecture" : f"{uri}/{kwards['project_name']}/{kwards['project_name']}.tf.json",
                        "project_location" : f"{uri}/{kwards['project_name']}",
                        "branch" : "",
                        "firstcommit" : 0
                    }
                },_file)
            with open(f"{uri}/{kwards['project_name']}/buildspec.yml", "w") as _file:
                file_ = str(f"version: 0.2\n\n\
phases:\n\
  build:\n\
    commands:\n\
      - echo Build started on `date`\n\
      - echo Building the Docker image...\n\
      - echo $IMAGE_TAG\n\
      - echo $IMAGE_REPO\n\
      - docker build -f Dockerfile.train -t '{kwards['project_name']}-ecr-datup:train_branch' .\n\
      - docker tag '{kwards['project_name']}-ecr-datup:train_branch' '147018152776.dkr.ecr.us-east-1.amazonaws.com/{kwards['project_name']}-ecr-datup:train_branch'\n\
      - docker build -f Dockerfile.pred -t '{kwards['project_name']}-ecr-datup:pred_branch' .\n\
      - docker tag '{kwards['project_name']}-ecr-datup:pred_branch' '147018152776.dkr.ecr.us-east-1.amazonaws.com/{kwards['project_name']}-ecr-datup:pred_branch'\n\
  install:\n\
    runtime-versions:\n\
      docker: 18\n\
  post_build:\n\
    commands:\n\
      - echo Build completed on `date`\n\
      - echo Pushing the Docker image...\n\
      - docker push '147018152776.dkr.ecr.us-east-1.amazonaws.com/{kwards['project_name']}-ecr-datup:train_branch'\n\
      - docker push '147018152776.dkr.ecr.us-east-1.amazonaws.com/{kwards['project_name']}-ecr-datup:pred_branch'\n\
  pre_build:\n\
    commands:\n\
      - echo Logging in to Amazon ECR...\n\
      - $(aws ecr get-login --no-include-email --region $AWS_DEFAULT_REGION)")
                _file.write(file_)
            with open(f"{uri}/{kwards['project_name']}/Dockerfile.train", "w") as _file:
                file_ = str(f"FROM python:3.8\n\n\
RUN pip install sagemaker-containers boto3 sagemaker numpy scipy scikit-learn pandas statsmodels==0.11.0 datetime s3fs requests gitpython xlsxwriter xlrd datup pandas-profiling\n\n\
COPY {kwards['project_name']}/clean/* /opt/ml/code/{kwards['project_name']}/clean/*\n\
COPY {kwards['project_name']}/prepare/* /opt/ml/code/{kwards['project_name']}/prepare/*\n\
COPY {kwards['project_name']}/transform/* /opt/ml/code/{kwards['project_name']}/transform/*\n\
COPY {kwards['project_name']}/train/* /opt/ml/code/{kwards['project_name']}/train/*\n\
COPY {kwards['project_name']}/routes.py /opt/ml/code/{kwards['project_name']}/routes.py\n\
COPY {kwards['project_name']}/training.py /opt/ml/code/{kwards['project_name']}/training.py\n\n\
ENTRYPOINT python3 /opt/ml/code/{kwards['project_name']}/training.py")
                _file.write(file_)
            with open(f"{uri}/{kwards['project_name']}/Dockerfile.pred", "w") as _file:
                file_ = str(f"FROM python:3.8\n\n\
RUN pip install sagemaker-containers boto3 sagemaker numpy scipy scikit-learn pandas statsmodels==0.11.0 datetime s3fs requests gitpython xlsxwriter xlrd datup pandas-profiling\n\n\
COPY {kwards['project_name']}/inference/* /opt/ml/code/{kwards['project_name']}/inference/*\n\
COPY {kwards['project_name']}/routes.py /opt/ml/code/{kwards['project_name']}/routes.py\n\
COPY {kwards['project_name']}/predicting.py /opt/ml/code/{kwards['project_name']}/predicting.py\n\n\
ENTRYPOINT python3 /opt/ml/code/{kwards['project_name']}/predicting.py")
                _file.write(file_)
            with open(f"{uri}/{kwards['project_name']}/manage.py", "w") as _file:
                file_ = str("import argparse\n\
import json\n\
import os\n\
from re import findall\n\
import sys\n\
import boto3\n\
import time\n\n\
class MainCommands:\n\
    def __init__(self):\n\
        pass\n\n\
    def runproject_paremeters(self, image, base_name, instance_type='ml.t3.medium'):\n\
        sm_ = boto3.client('sagemaker',aws_access_key_id='AKIASEOXW7NEFSICQG7B', aws_secret_access_key='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', region_name='us-east-1')\n\
        def get_unique_job_name(base_name: str):\n\
            timestamp = time.strftime('%Y%m%d-%H%M%S')\n\
            return f'{base_name}-{timestamp}'\n\
        job_name = get_unique_job_name(base_name)\n\
        processingjob = sm_.create_processing_job(\n\
                ProcessingJobName=job_name,\n\
                ProcessingResources={\n\
                    'ClusterConfig': {\n\
                        'InstanceCount': 1,\n\
                        'InstanceType': instance_type,\n\
                        'VolumeSizeInGB': 1,\n\
                    }\n\
                },\n\
                AppSpecification={\n\
                    'ImageUri': image,\n\
                },\n\
                RoleArn='arn:aws:iam::147018152776:role/service-role/AmazonSageMaker-ExecutionRole-20190522T173392'\n\
            )\n\
        return processingjob\n\n\
    def runproject(self):\n\
        image = str(input('Enter the uri of the image: '))\n\
        base_name = str(input('Enter the name of the sagemaker process: '))\n\
        instance = str(input('Do you want to choose a type of instance?. If not the ml.t3.medium is the instance as default [y/N]: '))\n\
        if instance == 'y' :\n\
            instance_type = str(input('Enter the type of the instance which you want to use: '))\n\
            sagemaker_job = self.runproject_paremeters(image, base_name, instance_type)\n\
        else :\n\
            sagemaker_job = self.runproject_paremeters(image, base_name)\n\
        print(sagemaker_job)\n\n\
    def add(self, first, project):\n\
        if first:\n\
            os.system(f'git add *')\n\
        else:\n\
            os.system(f'git add {project}/* Dockerfile.pred Dockerfile.train buildspec.yml')\n\n\
    def commit(self, first):\n\
        if first:\n\
            description = 'This is the first commit from datupie SW framework'\n\
        else:\n\
            description = str(input('Description of commit: '))\n\
        os.system(f'git commit -m "'"{description}"'"')\n\n\
    def create_branch(self, branch, first):\n\
        if first:\n\
            os.system(f'git checkout -b {branch}')\n\
        else:\n\
            os.system(f'git branch {branch}')\n\n\
    def push(self, branch,first):\n\
        if first:\n\
            os.system(f'git push --set-upstream origin {branch}')\n\
        else:\n\
            os.system(f'git push origin {branch}')\n\
            os.system(f'git push')\n\n\
    def pull(self,branch):\n\
        f = self.settings_project()\n\
        branch = f['metadata']['branch']\n\
        pull = str(input('Please be sure if you want to do this, whether you continue your local files could be replaced for the production enviroment files, do you want to continue [y/N]: '))\n\
        if pull == 'y':\n\
            os.system(f'git pull {branch}')\n\n\
    def settings_project(self):\n\
        with open('project.json', 'r') as _file:\n\
            f = json.load(_file)\n\
        return f\n\n\
    def settings_yml(self):\n\
        with open('buildspec.yml', 'r') as _file:\n\
            yml = _file.read()\n\
        return yml\n\n\
    def pylintscore_validation(self):\n\
        with open('pylint.log') as _file:\n\
            score_line = _file.read()\n\
            score = float(findall(r'([0-9\.]+)/10', score_line)[0])\n\
        return score\n\n\
    def firstcommit(self):\n\
        f = self.settings_project()\n\
        yml = self.settings_yml()\n\
        if f['metadata']['firstcommit'] == 1:\n\
            print('The firstcommit previously exists, developer branch must also exists, you may do a regularcommit')\n\
        else:\n\
            verify_if_create_clone = str(input('Did you create or clone the project, if created it please type CREATED but if cloned it please type CLONED: '))\n\
            branch_name = str(input('Please enter the name of the branch in developer mode: '))\n\
            first = False\n\
            if verify_if_create_clone == 'CREATED':\n\
                default_branch = 'master'\n\
                first = True\n\
                self.create_branch(default_branch, first)\n\
                self.add(first, None)\n\
                self.commit(first)\n\
                self.push(default_branch, first)\n\
            else : pass\n\
            yml = yml.replace('train_branch',f'train_{branch_name}').replace('pred_branch',f'pred_{branch_name}')\n\
            with open('buildspec.yml', 'w') as _file:\n\
                _file.write(yml)\n\
            f['metadata']['firstcommit'] = 1\n\
            f['metadata']['branch'] = branch_name\n\
            with open('project.json', 'w') as _file:\n\
                json.dump(f,_file)\n\
            self.create_branch(f['metadata']['branch'], first)\n\
            project = str(f['metadata']['project'])\n\
            self.add(first, project)\n\
            self.commit(True)\n\
            self.push(f['metadata']['branch'], first)\n\n\
    def regularcommit(self):\n\
        f = self.settings_project()\n\
        if f['metadata']['firstcommit'] == 0:\n\
            print('There is not exists a firstcommit, before doing a regularcommit please do a firstcommit first')\n\
        else:\n\
            os.system(f'pylint {project} --rcfile .pylintrc > pylint.log')\n\
            score = self.pylintscore_validation()\n\
            if float(score) >= 9.5:\n\
                first = False\n\
                project = f['metadata']['project']\n\
                self.add(first,project)\n\
                self.commit(first)\n\
                self.push(f['metadata']['branch'], first)\n\
            else :\n\
                print(f'There are errors with your syntax. Please check pylint.log. Your score was {score}')\n\
                sys.exit(0)\n\
if __name__ == '__main__':\n\
    FUNCTION_MAP = {\n\
        'firstcommit': MainCommands().firstcommit,\n\
        'regularcommit': MainCommands().regularcommit\n\
    }\n\
    parser = argparse.ArgumentParser()\n\
    parser.add_argument('command', choices=FUNCTION_MAP.keys())\n\
    args = parser.parse_args()\n\
    func = FUNCTION_MAP[args.command]\n\
    func()")
                _file.write(file_)

            with open(f"{uri}/{kwards['project_name']}/.pylintrc", "w") as _file:
                _file.write("[MASTER]\n\n\
profile=no\n\
ignore=.svn\n\
persistent=yes\n\
cache-size=500\n\
load-plugins=\n\
disable=C0114,C0116,W1203,R0912,R0915\n\
[MESSAGES CONTROL]\n\n\
disable-msg=C0323,W0142,C0301,C0103,C0111,E0213,C0302,C0203,W0703,R0201\n\
[REPORTS]\n\n\
output-format=colorized\n\
include-ids=yes\n\
files-output=no\n\
reports=yes\n\
evaluation=10.0 - ((float(5 * error + warning + refactor + convention) / statement) * 10)\n\
comment=no\n\
[VARIABLES]\n\n\
init-import=no\n\
dummy-variables-rgx=_|dummy\n\
additional-builtins=\n\
[TYPECHECK]\n\n\
ignore-mixin-members=yes\n\
zope=no\n\
acquired-members=REQUEST,acl_users,aq_parent\n\
[BASIC]\n\n\
required-attributes=\n\
no-docstring-rgx=__.*__\n\
module-rgx=(([a-z_][a-z0-9_]*)|([A-Z][a-zA-Z0-9]+))$\n\
const-rgx=(([A-Z_][A-Z1-9_]*)|(__.*__))$\n\
class-rgx=[A-Z_][a-zA-Z0-9]+$\n\
function-rgx=[a-z_][a-z0-9_]{2,30}$\n\
method-rgx=[a-z_][a-z0-9_]{2,30}$\n\
attr-rgx=[a-z_][a-z0-9_]{2,30}$\n\
argument-rgx=[a-z_][a-z0-9_]{2,30}$\n\
variable-rgx=[a-z_][a-z0-9_]{2,30}$\n\
inlinevar-rgx=[A-Za-z_][A-Za-z0-9_]*$\n\
good-names=i,j,k,ex,Run,_\n\
bad-names=foo,bar,baz,toto,tutu,tata\n\
bad-functions=apply,input\n\
[DESIGN]\n\n\
max-args=12\n\
max-locals=30\n\
max-returns=12\n\
max-branchs=30\n\
max-statements=60\n\
max-parents=7\n\
max-attributes=20\n\
min-public-methods=0\n\
max-public-methods=20\n\
[IMPORTS]\n\n\
deprecated-modules=regsub,string,TERMIOS,Bastion,rexec\n\
import-graph=\n\
ext-import-graph=\n\
int-import-graph=\n\
[CLASSES]\n\n\
ignore-iface-methods=isImplementedBy,deferred,extends,names,namesAndDescriptions,queryDescriptionFor,getBases,getDescriptionFor,getDoc,getName,getTaggedValue,getTaggedValueTags,isEqualOrExtendedBy,setTaggedValue,isImplementedByInstancesOf,adaptWith,is_implemented_by\n\
defining-attr-methods=__init__,__new__,setUp\n\
[SIMILARITIES]\n\n\
min-similarity-lines=10\n\
ignore-comments=yes\n\
ignore-docstrings=yes\n\
[MISCELLANEOUS]\n\
notes=FIXME,XXX,TODO\n\
[FORMAT]\n\n\
max-line-length=200\n\
max-module-lines=1000\n\
indent-string='    '\n\
indent-after-paren=4")

        else : print(response_status.text)
