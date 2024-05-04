import sqlite3
import hashlib

ACCOUNTS_TABLE = "accounts"
USERNAME_COLUMN = "username"
PASSWORD_COLUMN = "password"


class DatabaseHelper(sqlite3.Connection):

    def __init__(self, database_path: str) -> None:

        super().__init__(
            database=database_path, check_same_thread=False
        )

    def execute(self, sql: str, parameters) -> sqlite3.Cursor:
        return super().execute(sql, parameters)

    def add_account(self, username, password):
        if username == "" or password == "":
            return

        self.execute(
            f"INSERT INTO {ACCOUNTS_TABLE} ({USERNAME_COLUMN}, {PASSWORD_COLUMN}) VALUES (?, ?)",
            (username, DatabaseHelper.hash_password(password))
        )
        super().commit()

    def account_valid(self, username, password):
        if username == "" or password == "":
            return False

        user = self.execute(
            f"SELECT * FROM {ACCOUNTS_TABLE} WHERE {USERNAME_COLUMN} = ? AND {PASSWORD_COLUMN} = ?",
            (username, DatabaseHelper.hash_password(password))).fetchone()

        return user is not None
    """
        Returns true when an account exists with the provided username
    """

    def account_exists(self, username):
        if username == "":
            return True

        user = self.execute(
            f"SELECT * FROM {ACCOUNTS_TABLE} WHERE {USERNAME_COLUMN} = ?",
            (username,)).fetchone()

        return user is not None

    @staticmethod
    def hash_password(password: str) -> str:
        algo = hashlib.sha256()
        algo.update(password.encode())
        return algo.hexdigest()
