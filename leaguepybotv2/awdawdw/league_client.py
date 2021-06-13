from leaguepybotv2.logger.logger import get_logger

logger = get_logger()


class LeagueClient:
    def __init__(self):
        self.connector = Connector()

    async def _request(self, *args, **kwargs):
        print(kwargs)
        response = await self.connection.request(**kwargs)
        if response.status != 200:
            raise ValueError
        response = await response.json()
        return response

    async def get_summoner_data(self, *args, **kwargs):
        data = await self._request(
            method="GET", endpoint="/lol-summoner/v1/current-summoner"
        )
        logger.info(f"displayName:    {data['displayName']}")
        logger.info(f"summonerId:     {data['summonerId']}")
        logger.info(f"puuid:          {data['puuid']}")
        logger.info("-")

    async def get_lockfile(self, *args, **kwargs):
        import os

        path = os.path.join(
            self.connection.installation_path.encode("gbk").decode("utf-8"), "lockfile"
        )
        if os.path.isfile(path):
            file = open(path, "r")
            text = file.readline().split(":")
            file.close()
            logger.info(self.connection.address)
            logger.info(f"riot    {text[3]}")
            return text[3]
        return None

    async def login(self, *args, **kwargs):
        response = await self._request(**kwargs)
        if response.get("httpStatus") == 200:
            logger.warning("Logged in")
        else:
            logger.warning("Already logged in")
