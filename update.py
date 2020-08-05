import subprocess
import sys
import os
import time

from datetime import datetime, timedelta
from itertools import groupby

from cloc_videos import get_total_duration


DL_PATH = ".\\Filmy"
lastUpdated = 20200801

commands = [
    "youtube-dl --dateafter " + str(lastUpdated),  # aktualizuje
    "youtube-dl",  # pobiera po raz pierwszy
    "youtube-dl --extract-audio --audio-format mp3 --dateafter " + str(lastUpdated)  # podcasty
]

FNAME = 0
LINK = 1
CID = 2

class YoutubeDownloader:
    def __init__(self):
        self.dir_path = os.path.dirname(os.path.realpath(__file__))
        self.downloadedItems = []
        self.stop_downloading = 0

        self.channels_list = []
        self.ignored_channels_list = []
        self.load_channels_list()


    def youtube_update(self):
        self.executeCommand("youtube-dl -U")

    def executeCommand(self, cmd):
        curItem = ""
        process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        while True:
            if process.poll() is not None:
                break

            nextline = process.stdout.readline()

            if nextline != '':
                nextline = nextline.decode("utf-8", errors="ignore")

            sys.stdout.write(nextline)
            sys.stdout.flush()

            if "No space left on device" in nextline:
                self.stop_downloading = 1
                break

            if "upload date is not in range" in nextline:
                break

            if "Destination:" in nextline:
                curItem = nextline.split("Destination:")[1]

            if "100%" in nextline and curItem != "":
                self.downloadedItems.append(curItem)
                curItem = ""

        process.stdout.close()
        process.terminate()
        print("")


    def item_cid(self, item):
        if len(item) > CID:
            return int(item[CID])

        return 0

    def download_items(self):
        print("DL_PATH={}".format(DL_PATH))
        os.chdir(DL_PATH)
        self.executeCommand("cd")
        for item in self.channels_list:
            if not os.path.exists(item[FNAME]):
                os.makedirs(item[FNAME])

            if self.stop_downloading == 1:
                continue

            command = commands[self.item_cid(item)]

            cmd = "cd " + item[FNAME] + " && "
            cmd += command + " " + item[LINK] + " && "
            cmd += "cd .."
            print("*" * 40 + " " + item[FNAME].upper() + " " + "*" * 40)
            print(cmd)

            self.executeCommand(cmd)

        os.chdir('..')

    def update_data(self):
        if self.stop_downloading:
            return

        lines_to_write = []
        for item in self.channels_list + self.ignored_channels_list:
            if not item[FNAME].startswith("#"):
                cid = self.item_cid(item)
                if cid == 1:
                    item.pop()

            lines_to_write.extend(item)
            lines_to_write.append("")

        with open("{}\\channels_list.txt".format(self.dir_path), "wt") as f:
            f.write('\n'.join(lines_to_write))

        newDate = "lastUpdated = " + str((datetime.today() - timedelta(1)).strftime('%Y%m%d')) + '\n'
        with open(os.path.basename(__file__), "r") as file:
            lines = file.readlines()

            for index, item in enumerate(lines):
                if item.startswith("lastUpdated"):
                    lines[index] = newDate
                    break

        with open(os.path.basename(__file__), "w") as f:
            f.write(''.join(lines))

        print(newDate)

    def load_channels_list(self):
        with open("{}\\channels_list.txt".format(self.dir_path), "rt") as f:
            lines = f.read().splitlines()

        self.channels_list = [list(group) for k, group in groupby(lines, lambda x: x == "") if not k]
        self.ignored_channels_list = list(filter(lambda x: x[0].startswith("#"), self.channels_list))
        self.channels_list = list(filter(lambda x: not x[0].startswith("#"), self.channels_list))


if __name__ == '__main__':
    startTime = time.time()

    yt = YoutubeDownloader()
    yt.youtube_update()
    yt.download_items()
    yt.update_data()

    for line in yt.downloadedItems:
        print(line.replace("\n", "").strip().split('__', 1)[1])
    print('Downloaded {} files'.format(len(yt.downloadedItems)))


    print(time.strftime("%Mm %Ss", time.gmtime(time.time() - startTime)))
    print()

    get_total_duration(DL_PATH)
