from leaguepybot.client.connection.lockfile import Lockfile


class Connection:
    def __init__(self):
        self.lockfile = Lockfile.get_instance()
        self.headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
        }
