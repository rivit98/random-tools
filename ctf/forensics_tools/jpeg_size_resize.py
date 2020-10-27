import struct
import io
import sys
from shutil import copyfile


def get_img_size(fname):
    with open(fname, 'rb') as dafile:
        jpeg = io.BytesIO(dafile.read())

    try:
        type_check = jpeg.read(2)
        if type_check != b'\xff\xd8':
            print("Not a JPG")
        else:
            byte = jpeg.read(1)

            while byte != b"":
                while byte != b'\xff':
                    byte = jpeg.read(1)

                while byte == b'\xff':
                    byte = jpeg.read(1)

                if b'\xC0' <= byte <= b'\xC3':
                    jpeg.read(3)
                    o = jpeg.tell()
                    h, w = struct.unpack('>HH', jpeg.read(4))
                    break
                else:
                    jpeg.read(int(struct.unpack(">H", jpeg.read(2))[0]) - 2)

                byte = jpeg.read(1)

            width = int(w)
            height = int(h)
            offset = int(o)

            print("Width: {}, Height: {} | Offset: {}".format(width, height, hex(offset)))
            return width, height, offset
    finally:
        jpeg.close()


def modify_image(fname, newheight, offset):
    basename = fname.rsplit('.jpg', 1)[0]
    newname = "{}_{}.jpg".format(basename, newheight)
    copyfile(fname, newname)
    with open(newname, "r+b") as f:
        f.seek(offset)
        f.write(struct.pack(">H", newheight))

    print("Saved!")


if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("Usage: script.py image_path.jpeg cut_by_height")
        sys.exit(1)

    fname = sys.argv[1]
    cut_by = int(sys.argv[2])
    w, h, o = get_img_size(fname)
    if cut_by:
        h -= cut_by
        print("New height {}".format(h))
        modify_image(fname, h, o)
        get_img_size(fname)



