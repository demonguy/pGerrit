class GerritError(Exception):
    def __init__(self, status, content):
        self.status = status
        self.content = content