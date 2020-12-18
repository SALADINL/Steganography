#!/usr/bin/env python3

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

if not os.path.isfile(args.file):
    print('The file doesn\'t exist')
    sys.exit()

if ".png" not in args.file:
    print('The file isn\'t a PNG file.')
    sys.exit()

if args.filename is not None:
    if ".txt" not in args.filename:
        print('The file isn\'t a TXT file.')
        sys.exit()


def split_by1(bin_message):
    """
    Returns an array list with each element has only two digits.

    :param: bin_message : (str) A array list of ascii in binary
    :return: array_split : (str) A array list split in 1 digits
    """
    array_split = []
    for ele in bin_message:
        array_split += ele

    return array_split


def seq2bin(sequence):
    """
    Returns an array list of ascii in binary.

    :param sequence : (str) A array list split in 1 digits
    :return: array : (str) A array list of ascii in binary
    """
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
    """
    This function replace the latest lower-weight bytes of each channel (Alpha included) by
    two digits of the message we want to hide.

    :param pixels_rows : (str) An array list of pixels in binary [r , g , b , Alpha ... ], .., [r , g , b , Alpha ... ]
    :param bin_message : (str) An array list of ascii in binary
    :return: resp : (int) A array list of integer which is the new image with the hiding message.
    """

    sequence = split_by1(bin_message)
    for i in range(16):
        sequence += '0'  # Add an bytes with all bits a 0 to detect end of the message
    idx = 0

    resp = []
    for row in pixels_rows:
        array = []
        for ele in row:
            if idx < len(sequence):
                if sequence[idx] is not None:
                    array.append(int(ele[:len(ele) - 1] + sequence[idx], 2))
            else:
                array.append(int(ele, 2))
            idx += 1
        resp.append(array)
    return resp


def revel_data(pixels_rows):
    """
    This function read and save this last 2 digits of each channels until it find sixteen "0" following and stop.

    :param pixels_rows : (str) An array list of pixels in binary [r , g , b , Alpha ... ], .., [r , g , b , Alpha ... ]
    :return: Return an array list of ascii binary ['01110100', .. ]
    """

    sequence = []
    count_end = 0

    for row in pixels_rows:
        for ele in row:
            octt = str(ele)
            if count_end == 16:
                break
            if octt[len(octt) - 1: len(octt)] == "0":
                count_end += 1
            else:
                count_end = 0
            sequence.append(octt[len(octt) - 1: len(octt)])

    return seq2bin(sequence[:len(sequence) - 8])


def str2bin(message):
    """
    Convert string to an array list of ascii in binary

    :param message: (str) A string which contains the message
    :return: Returns array list of ascii in binary
    """

    bin_array = []

    for ele in message:
        bin_array.append(bin(ord(ele))[2:].zfill(8))

    return bin_array


def bin2str(bin_array):
    """
    Convert an array list of ascii in binary to  string

    :param bin_array: (str) An array list of ascii in binary
    :return: Returns string which contains the message
    """

    message = ""

    for ele in bin_array:
        message += chr(int(ele, 2))

    return message


def save_output(pixels_rows, filename):
    """
    This function will save le new image.

    :param pixels_rows : (str) An array list of pixels in binary [r , g , b , Alpha ... ], .., [r , g , b , Alpha ... ]
    :param filename: (str) Path of the file where we want to save our work.
    :return: None
    """

    newImage = png.from_array(pixels_rows, 'RGBA')
    newImage.save(filename)


def img2rgba(file_png):
    """
    This function open and read a png file to convert in an array list of pixels. FORMAT (RGBA)

    :param file_png: Path of png target
    :return: array_list : (str) An array list of pixels in binary [r , g , b , Alpha ... ], .., [r , g , b , Alpha ... ]
    """
    reader = png.Reader(filename=args.file)
    array_list = []

    for row in reader.asRGBA()[2]:
        array = []
        p = []
        for e in row:
            p.append(str(bin(e))[2:].zfill(8))
            array.append(str(bin(e)[2:].zfill(8)))
        array_list.append(array)
    return array_list


def read_txt(filename):
    """
    This function read a txt file and store it in a string.

    :param filename: Path of the txt file.
    :return: Return a string within the message
    """

    response = ""
    file = open(filename, 'r')
    response = file.read()
    file.close()

    return response


def check_space(message, pixels_rows):
    """
    This function evaluate if the message will fit in the file.

    :param message: (str) A string which contains the message.
    :param pixels_rows: (str) An array list of pixels in binary [r , g , b , Alpha ... ], .., [r , g , b , Alpha ... ]
    :return: Return True if the message has enough space in the container.
    """

    nb_bytes_needed = (len(message) * 8) + 16
    nb_bytes_free = len(pixels_rows[0]) * len(pixels_rows)

    return False if nb_bytes_needed > nb_bytes_free else True


def main():
    pixels_rows = img2rgba(args.file)

    if args.write:
        if args.filename:
            message = read_txt(args.filename)
        elif args.text:
            message = args.text
        else:
            message = input("Enter your message : ")

        if not check_space(message, pixels_rows):
            print("Your message is  to big for the container !")
            print("The program will stop.")
            sys.exit(0)

        newFile = hide_data(pixels_rows, str2bin(message))
        save_output(newFile, args.file)
    else:
        message = bin2str(revel_data(pixels_rows))
        print("Hiding message :")
        print(message)


if __name__ == '__main__':
    main()
