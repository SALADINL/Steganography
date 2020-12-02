import argparse
import os
import sys
import png

parser = argparse.ArgumentParser(description='This program provide tools to crypt and uncrypt message in PNG.',
                                 epilog='Enjoy the program!')
parser.add_argument("-w", "--write", help="enable writing mode into a png", action="store_true")

parser.add_argument("file", help="file in PNG format", action="store", type=str)

group = parser.add_mutually_exclusive_group()
group.add_argument("-f", "--filename", help="text to be inserted from the file filename", action="store", type=str)
group.add_argument("-t", "--text", help="text to be inserted from the the command line", action="store", type=str)
args = parser.parse_args()

if args.write:
    # TODO function writing
    pass
if args.text:
    print(args.text)
    print(args.file)

if not os.path.isfile(args.file):
    print('The file doesn\'t exist')
    sys.exit()

if ".png" not in args.file:
    print('The file isn\'t a PNG')
    sys.exit()

if args.text is not None:
    if ".txt" not in args.text:
        print('The file isn\'t a TXT')
        sys.exit()


def split_by2(bin_message):
    array_split = []
    for ele in bin_message:
        array_split += [ele[i:i + 2] for i in range(0, len(ele), 2)]

    return array_split


def seq2bin(sequence):
    array = []
    count = 0

    binascii = ""
    for ele in sequence:
        binascii += ele
        if len(binascii) == 8:
            array.append(binascii)
            binascii = ""

    return array


def hide_data(pixels_rows, bin_message):
    sequence = split_by2(bin_message)
    sequence += ['00', '00', '00', '00', '00', '00']
    idx = 0

    resp = []
    for row in pixels_rows:
        array = []
        for bin in row:
            if idx < len(sequence):
                if sequence[idx] is not None:
                    array.append(int(bin[:len(bin) - 2] + sequence[idx], 2))
            else:
                array.append(int(bin, 2))
            idx += 1
        resp.append(array)
    return resp


def revel_data(pixels_rows):
    sequence = []
    count_end = 0

    for row in pixels_rows:
        for ele in row:
            oct = str(bin(ele))[2:].zfill(8)
            # print(oct[len(oct) - 2: len(oct)])
            if count_end == 6:
                break
            if oct[len(oct) - 2: len(oct)] == "00":
                count_end += 1
            else:
                count_end = 0
            sequence.append(oct[len(oct) - 2: len(oct)])

    return seq2bin(sequence[:len(sequence)-6])


def str2bin(message):
    bin_array = []

    for ele in message:
        bin_array.append(bin(ord(ele))[2:].zfill(8))

    return bin_array


def bin2str(bin_array):
    message = ""

    for ele in bin_array:
        message += chr(int(ele, 2))

    return message


def save_output(pixels_rows, filename):
    newImage = png.from_array(pixels_rows, 'RGBA')
    newImage.save(filename)


if __name__ == '__main__':

    bin_message = str2bin("VICTOIRE")

    myImage = png.Reader(filename=args.file)
    array_list = []

    for row in myImage.asRGBA()[2]:
        array = []
        p = []
        for e in row:
            p.append(str(bin(e))[2:].zfill(8))
            array.append(str(bin(e)[2:].zfill(8)))
        array_list.append(array)

    resp = hide_data(array_list, bin_message)
    save_output(resp, "Mabite.png")

    bin_message2 = revel_data(resp)
    print(bin2str(bin_message2))