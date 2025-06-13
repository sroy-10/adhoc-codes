import asyncio

async def say_hello():
    print("Hello")
    
    await asyncio.sleep(1)
    # asyncio.sleep(1) ← this gives the error
    
    # same can be achieved using this
    # import time
    # time.sleep(2)
    
    print("World")

asyncio.run(say_hello())

# if the same needs to be executed from notebook, then
# await say_hello()
# because Jupyter Notebooks already run an event loop in the background, so asyncio.run() can't be used inside them.


async def wait_and_print():
    await asyncio.sleep(1)
    print("Done!")

async def main():
    # Without await, nothing happens
    wait_and_print()  # Missing await, coroutine is not run

    # This one actually runs
    await wait_and_print() # already inside an event loop in the background hence `await` is must

asyncio.run(main())
# asyncio.run(wait_and_print())  # this works too


# for multiple tasks

async def task(name, delay):
    print(f"Task {name} started")
    await asyncio.sleep(delay)
    print(f"Task {name} finished")

async def main():
    await asyncio.gather(
        task("A", 2),
        task("B", 1)
    )

asyncio.run(main())

