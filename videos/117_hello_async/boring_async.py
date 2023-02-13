import asyncio
import time


async def do_work(s: str, delay_s: float = 1.0):
    print(f"{s} started")
    await asyncio.sleep(delay_s)
    print(f"{s} done")


async def main():
    start = time.perf_counter()

    todo = ['get package', 'laundry', 'bake cake']

    tasks = [asyncio.create_task(do_work(item)) for item in todo]
    done, pending = await asyncio.wait(tasks)
    for task in done:
        result = task.result()

    tasks = [asyncio.create_task(do_work(item)) for item in todo]
    results = await asyncio.gather(*tasks, return_exceptions=True)

    coros = [do_work(item) for item in todo]
    results = await asyncio.gather(*coros, return_exceptions=True)

    async with asyncio.TaskGroup() as tg:  # Python 3.11+
        tasks = [tg.create_task(do_work(item)) for item in todo]

    end = time.perf_counter()
    print(f"it took: {end - start:.2f}s")


if __name__ == '__main__':
    asyncio.run(main())
