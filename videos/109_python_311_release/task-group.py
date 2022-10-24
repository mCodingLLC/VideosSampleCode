import asyncio

FAKE_ERRORS = False


async def update_db():
    if FAKE_ERRORS:
        raise ConnectionError


async def call_api():
    if FAKE_ERRORS:
        raise ValueError("quota exceeded")
    return {"id" : "1234", "data": "42"}


async def send_heartbeat():
    if FAKE_ERRORS:
        raise ConnectionError


async def do_the_thing():
    async with asyncio.TaskGroup() as tg:
        tg.create_task(update_db())
        call_api_task = tg.create_task(call_api())
        tg.create_task(send_heartbeat())

    print(f"API response: {call_api_task.result()}")


async def main():
    await do_the_thing()


if __name__ == "__main__":
    asyncio.run(main())
