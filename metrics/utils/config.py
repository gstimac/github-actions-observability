class Config:
    def __init__(self, db_host: str, db_password: str, db_user: str, webhook_secret: str):
        self.webhook_secret = webhook_secret
        self.db_user = db_user
        self.db_password = db_password
        self.db_host = db_host
