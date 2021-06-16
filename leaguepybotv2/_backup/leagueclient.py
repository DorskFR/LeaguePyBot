from lcu_driver import Connector
from random import randint
from leaguepybotv2.logger.logger import get_logger


logger = get_logger()


class LeagueClientConnector(Connector):
    def __init__(self):
        super().__init__()

    def __get__(self, obj, objtype):
        """Support instance methods."""
        super().__get__()
        import functools

        return functools.partial(self.__call__, obj)


class LeagueClient:
    connector = Connector()

    def __init__(self):
        self.connector.start()

    async def set_random_icon(self, connection=connector.connection):
        # random number of a chinese icon
        random_number = randint(0, 78)

        # make the request to set the icon
        icon = await connection.request(
            "put",
            "/lol-summoner/v1/current-summoner/icon",
            data={"profileIconId": random_number},
        )

        # if HTTP status code is 201 the icon was applied successfully
        if icon.status == 201:
            logger.info(f"Chinese icon number {random_number} was set correctly.")
        else:
            logger.error("Unknown problem, the icon was not set.")

    @connector.ready
    async def connect(self, connection=connector.connection):
        print("LCU API is ready to be used.")
        # check if the user is already logged into his account
        summoner = await connection.request("get", "/lol-summoner/v1/current-summoner")
        if summoner.status != 200:
            print(
                "Please login into your account to change your icon and restart the script..."
            )
        else:
            print("Setting new icon...")
            await self.set_random_icon(connection)

    @connector.ws.register("/lol-summoner/", event_types=("UPDATE",))
    async def summoner_updated(self, event):
        print(f'The summoner {event.data["displayName"]} was updated.')

    @connector.close
    async def disconnect(self):
        print("The client was closed")
        await self.connector.stop()


client = LeagueClient()
