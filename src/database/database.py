import pymongo


class DatabaseHelper():

    def __init__(self) -> None:
        self.client = pymongo.MongoClient("mongodb://localhost:27017/")
        self.database = self.client["agarpy"]
        self.accounts_collection = self.database["accounts"]

    def add_account(self, username, password):
        if username == "" or password == "":
            return
        account = {"username": username, "password": password}
        self.accounts_collection.insert_one(account)

    def account_valid(self, username, password):
        if username == "" or password == "":
            return False
        for document in self.accounts_collection.find():
            document_username = document["username"]
            document_password = document["password"]
            if document_username == username and document_password == password:
                return True
        return False

    """
        Returns true when an account exists with the provided username
    """

    def account_exists(self, username):
        if username == "":
            return True
        for document in self.accounts_collection.find():
            document_username = document["username"]
            if username == document_username:
                return True
        return False
