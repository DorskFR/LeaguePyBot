from LPBv2.controller import Controller
import asyncio


async def main():
    controller = Controller()
    await asyncio.sleep(5)
    await controller.shop.toggle_shop()
    await controller.shop.buy_item("ブラスティング ワンド")
    await controller.shop.buy_item("リデンプション")
    await controller.shop.buy_item("騎士の誓い")
    await controller.shop.buy_item("B. F. ソード")
    await controller.shop.buy_item("サファイア クリスタル")
    await controller.shop.buy_item("再生の珠")
    await controller.shop.toggle_shop()


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(main())
    finally:
        loop.close()