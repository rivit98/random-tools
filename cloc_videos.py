import sys
import os
import base64
import pickle
from pymediainfo import MediaInfo


def convert_milis(millis):
    h = millis / (1000 * 60 * 60)
    d = h / 24
    h %= 24
    return d, h


def load_db(path):
    try:
        with open(path, "rb") as f:
            return pickle.loads(f.read())
    except:
        return {}


def save_db(path, db):
    if(len(db) <= 0):
        return

    try:
        with open(path, "wb") as f:
            pickle.dump(db, f)
    except:
        pass


def dir_walk(start_dir):
    db_path = os.path.join(start_dir, ".cloc_videos_db")
    db = load_db(db_path)
    if(len(db) > 0):
        print("Found cache at: {}".format(db_path))

    new_db = {}
    files_num = 0
    total_duration = 0
    checked_files = 0
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
    return files_num, convert_milis(total_duration)


def get_total_duration(path):
    print("Scanning {}".format(path))
    files, (d, h) = dir_walk(path)
    print("\nTotal videos: {}".format(files))
    print("Total duration: {} days {} hours".format(int(d), int(h)))


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: cloc_videos.py path")
        sys.exit(1)

    get_total_duration(sys.argv[1])
