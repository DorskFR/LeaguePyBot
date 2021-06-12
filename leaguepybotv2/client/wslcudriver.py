from leaguepybotv2.lcu_driver import Connector
import asyncio


class LeagueClientConnector(Connector):
    def __init__(self):
        super().__init__()

    def __get__(self, obj, objtype):
        """Support instance methods."""
        super().__get__()
        import functools

        return functools.partial(self.__call__, obj)


class LeagueClient:
    def __init__(self):
        self.connector = Connector()
        self.ready = self.connector.ready()(self.func)

        @self.ready
        async def connect(connection):
            print("LCU API is ready to be used.")

        @self.connector.ws.register("/lol-summoner/", event_types=("UPDATE",))
        async def summoner_updated(connection, event):
            print(f'The summoner {event.data["displayName"]} was updated.{event.data}')

        @self.connector.close
        async def disconnect(connection):
            print("The client was closed")
            await self.connector.stop()


client = LeagueClient()
