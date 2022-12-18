import subprocess
import time

while True:
    time.sleep(1)
    subprocess.run(['xdotool', 'key', 'space'])


    # subprocess.run(["xdotool",
    #                 "key",
    #                 "--window", "\"$(xdotool search \"papers, please\" | head -1)\"",
    #                 "Escape"])

    #subprocess.run(['xdotool', 'search', '"papers, please"', 'windowactivate', '--sync', 'key', '--clearmodifiers', 'Escape'])
