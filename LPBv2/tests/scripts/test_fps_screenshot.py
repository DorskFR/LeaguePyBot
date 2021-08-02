from mss import mss
import numpy as np
import asyncio
import time


def measure_time(func):
    def time_it(*args, **kwargs):
        time_started = time.time()
        result = func(*args, **kwargs)
        time_elapsed = time.time()
        print(
            f"{func.__name__} running time is {round(time_elapsed - time_started, 10)} seconds."
        )
        return result

    return time_it


async def screenshot():
    with mss() as sct:

        return np.asarray(
            sct.grab(
                {
                    "top": 0,
                    "left": 0,
                    "width": 1920,
                    "height": 1080,
                }
            )
        )


async def main():
    loop_time = time.time()
    all_FPS = []
    while True:
        screen = await screenshot()
        all_FPS.append(round(float(1 / (time.time() - loop_time)), 2))
        average_FPS = sum(all_FPS) / len(all_FPS)
        print(f"Average FPS: {average_FPS}")
        loop_time = time.time()


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(main())
    finally:
        loop.close()
