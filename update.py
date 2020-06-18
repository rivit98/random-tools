import subprocess
import sys
import os
from datetime import datetime, timedelta
import time
from cloc_videos import get_total_duration

lastUpdated = 20200521

commands = [
    "youtube-dl --dateafter " + str(lastUpdated) + " ",  # aktualizuje
    "youtube-dl ",  # pobiera po raz pierwszy
    "youtube-dl --extract-audio --audio-format mp3 --dateafter " + str(lastUpdated) + " "  # podcasty
]

DL_PATH = "./Filmy"

itemsToDownload = [
    {
        "fname": "chilltomatonoodle",
        "link": "ytuser:ChiliTomatoNoodle"
    },
    {
        "fname": "liveoverflow",
        "link": "https://www.youtube.com/channel/UClcE-kVhqyiHCcjYwcpfj9w"
    },
    {
        "fname": "murmusctf",
        "link": "https://www.youtube.com/channel/UCUB9vOGEUpw7IKJRoR4PK-A"
    },
    {
        "fname": "ippsec",
        "link": "https://www.youtube.com/channel/UCa6eh7gCkpPo5XXUDfygQQA"
    },
    {
        "fname": "oalabs",
        "link": "https://www.youtube.com/channel/UC--DwaiMV-jtO-6EvmKOnqg"
    },
    {
        "fname": "c++weekly",
        "link": "https://www.youtube.com/user/lefticus1/videos"
    },
    {
        "fname": "ghidra_ninja",
        "link": "https://www.youtube.com/channel/UC3S8vxwRfqLBdIhgRlDRVzw"
    },
    {
        "fname": "corecpp",
        "link": "https://www.youtube.com/channel/UCE14XYFaK1fDTnOTqlOFrrQ"
    },
    {
        "fname": "grysztar",
        "link": "https://www.youtube.com/channel/UCs_OWSjmFntZqjzSpgJoBhA"
    },
    {
        "fname": "nes_javid",
        "link": "https://www.youtube.com/channel/UC-yuWVUplUJZvieEligKBkA/videos"
    },
    {
        "fname": "nes_javid",
        "link": "https://www.youtube.com/channel/UC77N7im6bfUPvR3PkRKaVGQ/videos"
    },
    {
        "fname": "cherno",
        "link": "https://www.youtube.com/channel/UCWBDJSwiF9YQGHdQ82rhw5g/videos",
    },
    {
        "fname": "RetroGameMechanicsExplained",
        "link": "https://www.youtube.com/channel/UCwRqWnW5ZkVaP_lZF7caZ-g/videos",
    },
    {
	    "fname": "john_hammond",
	    "link": "https://www.youtube.com/user/RootOfTheNull/videos"
    },
    {
    	"fname": "cherno",
    	"link": "https://www.youtube.com/user/TheChernoProject",
    },

    # {
    # "cid": 0,
    # "fname": "cppcon",
    # "link": "https://www.youtube.com/user/CppCon"
    # },
    # {
    # "cid": 0,
    # "fname": "sentdex",
    # "link": "https://www.youtube.com/user/sentdex"
    # },
    # {
    # "cid": 0,
    # "fname": "boostcon",
    # "link": "https://www.youtube.com/user/BoostCon/videos"
    # },

    # 
]

downloadedItems = []
dontWriteNewFile = 0


def dlItems():
    global dontWriteNewFile

    print("DL_PATH={}".format(DL_PATH))
    os.chdir(DL_PATH)
    executeCommand("cd")
    for item in itemsToDownload:
        if not os.path.exists(item["fname"]):
            os.makedirs(item["fname"])

        if dontWriteNewFile == 1:
            continue

        if "cid" in item:
            command = commands[item["cid"]]
        else:
            command = commands[0]

        cmd = "cd " + item["fname"] + " && "
        cmd += command + item["link"] + " && "
        cmd += "cd .."
        print("*" * 40 + " " + item["fname"].upper() + " " + "*" * 40)
        print(cmd)

        executeCommand(cmd)

    os.chdir('..')


def executeCommand(cmd):
    global dontWriteNewFile

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
            dontWriteNewFile = 1
            break

        if "upload date is not in range" in nextline:
            break

        if "Destination:" in nextline:
            curItem = nextline.split("Destination:")[1]

        if "100%" in nextline and curItem != "":
            downloadedItems.append(curItem)
            curItem = ""

    process.stdout.close()
    process.terminate()
    print("")


def updateDate():
    global dontWriteNewFile

    if dontWriteNewFile:
        return

    replacer0 = '0'
    newDate = "lastUpdated = " + str((datetime.today() - timedelta(1)).strftime('%Y%m%d')) + '\n'
    with open(os.path.basename(__file__), "r") as file:
        lines = file.readlines()
        lines2 = []
        for line in lines:
            if "cid" in line and replacer0 in line and '#' not in line:
                continue

            lines2.append(line)

        lines = lines2

        for index, item in enumerate(lines):
            if item.startswith("lastUpdated"):
                lines[index] = newDate
            if "cid" in item and '1' in item and 'if' not in item:  # funny bug was here :D
                lines[index] = lines[index].replace('1', '0')

    with open(os.path.basename(__file__), "w") as f:
        f.write(''.join(lines))

    print(newDate)


def updateYtDl():
    executeCommand("youtube-dl -U")
    # time.sleep(20)


if __name__ == '__main__':
    startTime = time.time()
    updateYtDl()
    dlItems()
    updateDate()
    for line in downloadedItems:
        print(line.replace("\n", "").strip().split('__', 1)[1])
    print('Downloaded {} files'.format(len(downloadedItems)))
    print(time.strftime("%Mm %Ss", time.gmtime(time.time() - startTime)))
    print()

    get_total_duration(DL_PATH)
