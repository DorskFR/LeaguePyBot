import pytest
from LPBv2.common import LoopInNewThread
import concurrent.futures


@pytest.fixture
def get_loop():
    loop = LoopInNewThread()
    yield loop
    loop.stop_async()


def test_loop_init(get_loop):
    assert get_loop
    assert isinstance(get_loop, LoopInNewThread)
    assert hasattr(get_loop, "start_async")
    assert hasattr(get_loop, "submit_async")
    assert hasattr(get_loop, "stop_async")


async def say_hello():
    return "Hello"


def test_loop_submit_async(get_loop):
    coro = get_loop.submit_async(say_hello())
    assert isinstance(coro, concurrent.futures.Future)
