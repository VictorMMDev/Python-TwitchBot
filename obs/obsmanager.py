from .obs import OBS
import asyncio

class OBSMANAGER:
    def __init__(self):
        self.obs = OBS()
        self.queue = asyncio.Queue()
        self.videoon = False
        self.audioon = False
        self.playerruning = False

    def setscene(self, Grabar):
        self.obs.setscene(Grabar)


    async def showimage(self, scene: str, filename: str, duration: float, x: int, y: int, width: int, height: int):
        await self.enqueue(scene, filename, duration, x, y, width, height, False)


    async def playsoundorvideo(self, scene: str, filename: str, duration: float, x: int, y: int, width: int, height: int, video: bool = False):
        if video:
            await self.enqueue(scene, filename, duration, x, y, width, height, video)
            
        else:
            while self.videoon:
                await asyncio.sleep(0.1)
            self.audioon = True
            await self.obs.playsoundorvideo(scene, filename, duration, video)
            self.audioon = False


    async def enqueue(self, scene: str, filename: str, duration: float, x: int, y: int, width: int, height: int, video: bool = False):
        await self.queue.put((scene, filename, duration,video, x, y, width, height))
        if not self.playerruning:
            self.playerruning = True
            asyncio.create_task(self.mediaplayer()) # We create an independent coroutine for the player.


    async def mediaplayer(self):
        while not self.queue.empty():
            scene, filename, duration, video, x, y, width, height = await self.queue.get()
            while self.videoon:
                await asyncio.sleep(0.1)
            if video:
                self.videoon = True
                while self.audioon:
                    await asyncio.sleep(0.1)
                await self.obs.playsoundorvideo(scene, filename, duration, video, x, y, width, height)
            else:
                await self.obs.showimage(scene, filename, duration, x, y, width, height)

            if video:
                self.videoon = False
        self.playerruning = False