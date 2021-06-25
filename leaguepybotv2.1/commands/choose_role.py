from .client_call import ClientCall


class ChooseRole(ClientCall):
    def __init__(self, first: str, second: str):
        super().__init()
        self.first_role: str = first or "FILL"
        self.second_role: str = second or "FILL"

    async def build(self):
        self.method = "PUT"
        self.endpoint = (
            "/lol-lobby/v2/lobby/members/localMember/position-preferences",
        )
        self.payload = {
            "firstPreference": self.first_role,
            "secondPreference": self.second_role,
        }

    async def action(self, response: WebsocketEventResponse):
        print("Selected role")
