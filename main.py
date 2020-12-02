import argparse
import os
import sys

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

if ".txt" not in args.text:
    print('The file isn\'t a TXT')
    sys.exit()

if __name__ == '__main__':
    print(args.File)
