import os

class CloneCommand:
    def __init__(self):
        pass        

    def validation(self, local_location, project) -> bool:
        if os.path.exists(f"{local_location}/{project}") : return False
        else : return True            

    def cloneproject(self):
        clone = str(input("Enter the URI of project you want to clone: "))
        project = str(input("Enter the name of the project, remember this name will be added to the local location path: "))
        local_location = str(input(f"Enter the local location where you want to save the project without the last '/' and before {project} : "))
        if self.validation(local_location,project) : os.system(f"git clone {clone} {local_location}/{project}")
        else : print("Project already exists in local")