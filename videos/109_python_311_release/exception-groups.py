import asyncio


async def update_db():
    raise ConnectionError


async def call_api():
    raise ValueError("quota exceeded")


async def send_heartbeat():
    raise ConnectionError




async def do_the_thing():
    async with asyncio.TaskGroup() as tg:
        tg.create_task(update_db())
        api_task = tg.create_task(call_api())
        tg.create_task(send_heartbeat())

    print(f"result of API {api_task.result()}")


async def exception_groups_example():
    try:
        await do_the_thing()
    except* ConnectionError as eg:
        ...  # retry?
    except* ValueError as eg:
        for exc in eg.exceptions:
            print(f"Log the error: {exc}")


async def main():
    await exception_groups_example()


if __name__ == "__main__":
    asyncio.run(main())
