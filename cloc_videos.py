import sys
import os
import base64
import pickle
from pymediainfo import MediaInfo
import logging

cloc_logger = logging.getLogger('cloc-logger')
cloc_fileHandler = logging.FileHandler('history.log')
cloc_logger.addHandler(cloc_fileHandler)
cloc_logger.setLevel(logging.INFO)
formatter = logging.Formatter("%(asctime)s | %(message)s", "%Y-%m-%d %H:%M:%S")
cloc_fileHandler.setFormatter(formatter)
miliseconds_in_hour = 1000 * 60 * 60
miliseconds_in_day = miliseconds_in_hour * 24


def convert_milis(milis):
    d = milis // miliseconds_in_day
    h = (milis - (d * miliseconds_in_day)) // miliseconds_in_hour
    return d, h


def load_db(path):
    try:
        with open(path, "rb") as f:
            return pickle.loads(f.read())
    except:
        return {}


def save_db(path, db):
    if len(db) <= 0:
        return

    try:
        with open(path, "wb") as f:
            pickle.dump(db, f)
    except:
        print("Cannot save DB", path)


def dir_walk(start_dir):
    db_path = os.path.join(start_dir, ".cloc_videos_db")
    db = load_db(db_path)
    if len(db) > 0:
        print("Found cache at: {}".format(db_path))

    new_db = {}
    files_num, old_files_num = 0, len(db)
    total_duration = 0
    checked_files = 0
    old_total_duration = sum(db.values())
    for root, dirs, files in os.walk(start_dir):
        for file in files:
            if checked_files % 200 == 0:
                sys.stdout.write('.')
                sys.stdout.flush()

            checked_files += 1
            encoded_name = base64.b64encode(file.encode()).decode()

            if encoded_name in db:
                dur = db[encoded_name]
                total_duration += dur
                new_db[encoded_name] = dur
                files_num += 1
            else:
                media_info = MediaInfo.parse(os.path.join(root, file))
                for track in media_info.tracks:
                    if track.track_type == "Video":
                        dur = int(float(track.duration))
                        total_duration += dur
                        new_db[encoded_name] = dur
                        files_num += 1
                        break

    save_db(db_path, new_db)
    return (files_num, old_files_num), (total_duration, old_total_duration)



def get_total_duration(path):
    print("Scanning {}".format(path))
    (files, old_files), (total_milis, old_total_milis) = dir_walk(path)
    files_diff = files - old_files
    output_string = "Total videos: {}".format(files)
    if files_diff != 0:
        output_string += " ({}{})".format(
            "+" if files >= old_files else "",
            files_diff
        )
    print('\n' + output_string)
    cloc_logger.info(output_string)

    (d, h), (d_o, h_o) = convert_milis(total_milis), convert_milis(abs(total_milis - old_total_milis))
    output_string = "Total duration: {} days {} hours".format(d, h)

    if d_o != 0 or h_o != 0:
        output_string += " ({}{}{} hours)".format(
            "+" if total_milis >= old_total_milis else "-",
            "{} days ".format(d_o) if d_o > 0 else "",
            h_o,
        )

    print(output_string)
    cloc_logger.info(output_string)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: cloc_videos.py path")
        sys.exit(1)

    path_ = sys.argv[1]
    if not os.path.exists(path_):
        print("No such directory: " + path_)
        sys.exit(2)

    get_total_duration(path_)
