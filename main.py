import argparse
import os
import sys

parser = argparse.ArgumentParser(description='This program provide tools to crypt and uncrypt message in PNG.',
                                 epilog='Enjoy the program!')
parser.add_argument("-w", "--write", help="enable writing mode into a png", action="store_true")

parser.add_argument("File", help="file in PNG format", action="store", type=str)

group = parser.add_mutually_exclusive_group()
group.add_argument("-f", "--filename", help="text to be inserted from the file filename", action="store", type=str)
group.add_argument("-t", "--text", help="text to be inserted from the the command line", action="store", type=str)
args = parser.parse_args()

input_file = args.File

if args.write:
    # TODO function writing
    pass
if args.text:
    print(args.text)
    print(input_file)

if not os.path.isfile(input_file):
    print('The file doesn\'t exist')
    sys.exit()

if ".png" not in input_file:
    print('The file isn\'t a PNG')
    sys.exit()

if __name__ == '__main__':
    print(args.File)
