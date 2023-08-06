import asyncio
import os
import random
import signal
import time
from ycd.youtube.channel import get_videos
from .arguments import Arguments
from json.decoder import JSONDecodeError
from pathlib import Path
from .videoinfo import VideoInfo
from .exceptions import InvalidVideoIdException, NoContents, PatternUnmatchError
from .util import extract_video_id, checkpath
from . import util
from typing import List, Dict
from .youtube import channel
from .progressbar import ProgressBar
from . import dl
import sys

class Downloader:

    def __init__(self, dir_videos: set):
        self._dir_videos = dir_videos

    def video(self, video) -> None:
        is_complete = False
        video_id = extract_video_id(video.get('id'))
        try:
            if not os.path.exists(Arguments().output):
                raise FileNotFoundError
            separated_path = str(Path(Arguments().output)) + os.path.sep
            path = checkpath(separated_path + video_id + '.txt')
            # check if the video_id is already exists the output folder
            if video_id in self._dir_videos:
                # raise Exception(f"Video [{video_id}] is already exists in {os.path.dirname(path)}. Skip process.")
                print(f"Video [{video_id}] is already exists in {os.path.dirname(path)}. Skip process.")
                sys.argv = []
                return

            # time.sleep(random.random() * 2 + 2)
            print(
                f"\n"
                f"[title]    {video.get('title')}\n"
                f"[id]       {video_id}    [published] {video.get('time_published')}\n"
                f"[channel]  {video.get('author')}"
            )
            print(f"[path]     {path}  [duration]{video.get('duration')}")
            # if video.get("error"):
            #     # error getting video info in parse()
            #     # raise Exception(f"The video [{video_id}] may be private or deleted.")
            #     print(Exception(f"The video [{video_id}] may be private or deleted."))
            #     return

            duration = video["duration"]
            # pbar = ProgressBar(total=(duration * 1000), status="Extracting")
            if len(sys.argv)==0:
                sys.argv = ['--url', f'https://www.youtoube.com/watch?v={video_id}', '--hide_output']
            dl.dlmain(path, duration * 1000, video_id)

            # ex = Extractor(video_id,
            #         callback=pbar._disp,
            #         div=1)
            # signal.signal(signal.SIGINT, (lambda a, b: self.cancel(ex, pbar)))
            # data = ex.extract()
            # if data == []:
            #     raise NoContents()
            # pbar.reset("#", "=", total=1000, status="Rendering  ")
            # processor = HTMLArchiver(path, callback=pbar._disp)
            # processor.process(
            #     [{'video_id': None,
            #       'timeout': 1,
            #       'chatdata': (action["replayChatItemAction"]["actions"][0] for action in data)}]
            # )
            # processor.finalize()
            # pbar.close()
            # print("\nCompleted")

            # print()
            # if pbar.is_cancelled():
            #     raise Exception("\nThe extraction process has been discontinued.\n")

            is_complete = True

        except InvalidVideoIdException:
            print("Invalid Video ID or URL:", video_id)
        except NoContents as e:
            print('---' + str(e)[:80] + '---')
        except FileNotFoundError:
            print("The specified directory does not exist.:{}".format(
                Arguments().output))
            exit(0)
        except (JSONDecodeError, PatternUnmatchError) as e:
            print("{}:{}".format(e.msg, video_id))
            if Arguments().save_error_data:
                util.save(e.doc, "ERR_", ".dat")
        except Exception as e:
            print(type(e), str(e)[:80])
            raise
        finally:
            clear_tasks()
            return is_complete

    def videos(self, video_ids: List[int]) -> None:
        for i, video_id in enumerate(video_ids):
            print(f"\n{'-'*10} video:{i+1} of {len(video_ids)} {'-'*10}")
            if '[' in video_id or ']' in video_id:
                video_id = video_id.replace('[', '').replace(']', '')
            try:
                video = self.get_info(video_id)
                if video.get('error'):
                    continue
                self.video(video)
            except InvalidVideoIdException:
                print(f"Invalid video id: {video_id}")
                continue

    def channels(self, channels: List[str]) -> None:
        for i, ch in enumerate(channels):
            counter = 0
            for video in get_videos(channel.get_channel_id(ch)):
                if counter > Arguments().first - 1:
                    break
                print(
                    f"\n{'-'*10} channel: {i+1} of {len(channels)} / video: {counter+1} of {Arguments().first} {'-'*10}")
                ret = self.video(video)
                if ret:
                    counter += 1

    def cancel(self, ex, pbar) -> None:
        '''Called when keyboard interrupted has occurred.
        '''
        print("\nKeyboard interrupted.\n")
        if ex:
            ex.cancel()
        if pbar:
            pbar.cancel()
        exit(0)

    def get_info(self, video_id: str) -> Dict:
        video = dict()
        for i in range(3):
            try:
                info = VideoInfo(video_id)
                break
            except PatternUnmatchError:
                time.sleep(2)
                continue
        else:
            print(f"PatternUnmatchError:{video_id}")
            return {'error': True}

        video['id'] = video_id
        video['author'] = info.get_channel_name()
        video['time_published'] = "Unknown"
        video['title'] = info.get_title()
        video['duration'] = info.get_duration()
        return video


def clear_tasks():
    '''
    Clear remained tasks.
    Called when internal exception has occurred or
    after each extraction process is completed.
    '''
    async def _shutdown():
        tasks = [t for t in asyncio.all_tasks()
                if t is not asyncio.current_task()]
        for task in tasks:
            task.cancel()
            
    try:
        loop = asyncio.get_event_loop()
        loop.run_until_complete(_shutdown())
    except Exception as e:
        print(e)
