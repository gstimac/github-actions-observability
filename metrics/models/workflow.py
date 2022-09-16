
class Workflow:
    def __init__(self, workflow_id, repo_id, name, path, created_at, updated_at, data):
        self.updated_at = updated_at
        self.created_at = created_at
        self.path = path
        self.repo_id = repo_id
        self.data = data
        self.name = name
        self.workflow_id = workflow_id
