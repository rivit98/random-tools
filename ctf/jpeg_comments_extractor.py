import os
import sys

def findComments(path_string):
    output_dir = "{}_extracted_comments".format(os.path.basename(path_string))

    with open(path_string, "rb") as f:
        file_contents = f.read()

    if file_contents[0:2] != b'\xff\xd8':
        print("Not a jpeg file")
        return

    print("Extracting from [{}] to [{}]".format(path_string, output_dir))

    try:
        os.mkdir(output_dir)
    except:
        pass

    offset = 0
    number = 0
    while True:
        try:
            comment_block_start = file_contents.index(b'\xff\xfe', offset)
            comment_size = int.from_bytes(file_contents[comment_block_start+2:comment_block_start+4], "big")

            comment_block_start += 2  # skip header and size
            offset = comment_block_start+comment_size
            comment_contents = file_contents[comment_block_start+2:offset]

            # print(comment_contents)

            with open("{}/{}.bin".format(output_dir, number), "wb") as f:
                f.write(comment_contents)

            number += 1

        except ValueError:
            break

    print("Done! {} comments extracted".format(number))




if __name__ == "__main__":
    if len(sys.argv) == 2:
        findComments(sys.argv[1])
    else:
        print("script.py path/to/file.jpg")

