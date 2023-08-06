import asyncio
from typing import NoReturn
import datetime
from chronous.Architecture import BaseArchitecture
from chronous.events import EventContext, Setup, Init, Start, Close


class SampleArchitecture(BaseArchitecture):

    def __init__(self) -> None:
        super(SampleArchitecture, self).__init__(name="sample")

        # Registering events
        self.register_event(event=Setup())
        self.register_event(event=Init())
        self.register_event(event=Start())
        self.register_event(event=Close())

    def run(self) -> None:
        # Registering default lifecycle events
        # Start process.
        print("Starting process...")
        asyncio.run(self.process())

    async def process(self) -> NoReturn:
        await self.dispatch("setup")
        await self.dispatch("init")
        print('='*20)
        await self.dispatch("start", datetime.datetime.now())
        index: int = 0
        while index < 10:
            print("Looping!")
            index += 1
        await self.dispatch("close")
        print('='*20)


sample = SampleArchitecture()


# Multiple listener sample
@sample.listen()
async def setup(ec: EventContext):
    print("{e.name} phase - listener 1".format(e=ec.event))


@sample.listen()
async def setup(ec: EventContext):
    print("{e.name} phase - listener 2".format(e=ec.event))


# EventContext  sample
@sample.listen()
async def init(ec: EventContext):
    print("Initialization phase")
    print("Event : {e}".format(e=ec.event))


# Additional arguments sample
@sample.listen()
async def start(ec: EventContext, time: datetime):
    print("Starting process...")
    print("Starting at : {time}".format(time=time))


# Exception sample
@sample.listen()
async def close(ec: EventContext):
    print("Closing process...")
    print(f"Make an error : {1/0}")

sample.run()
