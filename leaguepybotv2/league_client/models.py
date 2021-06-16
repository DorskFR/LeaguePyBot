from pydantic import BaseModel
from typing import Optional, List, Union, Callable, Coroutine


class ClientResponse(BaseModel):
    data: Optional[Union[str, int, float, list, dict]]
    status_code: Optional[int]
    endpoint: Optional[str]


class WebsocketEvent(BaseModel):
    endpoint: str
    type: Union[str, List[str]]
    function: Callable
    arguments: Optional[Union[str, int, float, list, dict]]


class WebsocketEventResponse(BaseModel):
    type: str
    uri: str
    data: Optional[Union[str, int, float, list, dict]]


class Lockfile(BaseModel):
    lcu_pid: int
    pid: int
    port: int
    auth_key: str
    installation_path: str
