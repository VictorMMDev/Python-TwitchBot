import os
from dotenv import load_dotenv
from obsws_python import ReqClient
import asyncio
import uuid

load_dotenv()

HOST = os.getenv("OBS_HOST")
PORT = int(os.getenv("OBS_PORT"))
PASSWORD = os.getenv("OBS_PASSWORD")

if HOST is None or PORT is None or PASSWORD is None:
    raise ValueError("Error in .env (OBS).")

class OBS:

    def __init__(self):
        try:
            self.client = ReqClient(
                host=HOST,
                port=PORT,
                password=PASSWORD
            )
            print("Connected to OBS")
        except:
            print("Error on obs login.")

    def setscene(self, scene):
        self.client.set_current_program_scene(scene)

    async def showimage(self, scene: str, filename: str, duration: float = 5, x: int = 100, y: int= 200, width: int = 640, height: int = 360):
        source = f"IMG_{uuid.uuid4().hex[:8]}" # Random source name generator.
        try:
            path = os.path.join("obs", "images", filename)
            if not os.path.isfile(path):
                print("Media file not found.")
            
            self.client.create_input(scene, source, "image_source", {"file": os.path.abspath(path)}, True)
            response = self.client.get_scene_item_id(scene, source)
            sceneitemid = response.scene_item_id

            self.client.set_scene_item_transform(
                scene,
                sceneitemid,
                {
                    "positionX": x,
                    "positionY": y,
                    "width": width,
                    "height": height,
                }
            )

            await asyncio.sleep(duration)
        except Exception as e:
            print(f"OBS error while displaying {filename}: {e}")
        finally:
            try:
                self.client.remove_input(source)
            except Exception as e:
                print(f"OBS cleanup error for {source}: {e}")


    async def playsoundorvideo(self, scene: str, filename: str, duration: float = 5, video: bool = False, x: int = 100, y: int = 200, width: int = 640, height: int = 360):
        source = f"IMG_{uuid.uuid4().hex[:8]}" # Random source name generator.
        try:
            if video:
                path = os.path.join("obs", "videos", filename) # Video input.
            else:
                path = os.path.join("obs", "sounds", filename) # Audio input.
            if not os.path.isfile(path):
                print("Media file not found.")
            
            self.client.create_input(scene, source, "ffmpeg_source", {"local_file": os.path.abspath(path)}, True)

            if video:
                response = self.client.get_scene_item_id(scene, source)
                sceneitemid = response.scene_item_id

                self.client.set_scene_item_transform(
                    scene,
                    sceneitemid,
                    {
                        "positionX": x,
                        "positionY": y,
                        "width": width,
                        "height": height,
                    }
                )

            await asyncio.sleep(duration)
        except Exception as e:
            print(f"OBS error while displaying {filename}: {e}")
        finally:
            try:
                self.client.remove_input(source)
            except Exception as e:
                print(f"OBS cleanup error for {source}: {e}")