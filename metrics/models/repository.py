
class Repository:
    def __init__(self, repository_id, org_id, name, data):
        self.org_id = org_id
        self.data = data
        self.name = name
        self.repository_id = repository_id
