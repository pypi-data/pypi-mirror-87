class User:
    def __init__(self, api_key, container = None, sasToken = None):
        super().__init__()
        self.id:str
        self.api_key:str = api_key
        self.container:str = container
        self.sas_token: str = sasToken

    def setContainer(self, container):
        self.container:str = container
    
    def setAzureKey(self, id, key):
        self.azure_id:str = id
        self.azure_key:str = key

class Project:
    def __init__(self, project_name, workspace = None):
        super().__init__()
        self.workspace:str = workspace
        self.id:str
        self.auto_digo:str = 'none'
        self.name:str = project_name

class Experiment:
    def __init__(self):
        super().__init__()
        self.name:str
        self.id:str
        