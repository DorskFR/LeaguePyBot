from .lockfile import Lockfile


class Connection:
    def __init__(self):
        self.lockfile = Lockfile()
        self.headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
        }
