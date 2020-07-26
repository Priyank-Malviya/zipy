#!/usr/bin/env python3

from zipfile import ZipFile
import sys
import os
import datetime
from termcolor import colored
import time
import threading

def load_animation(str):
    load_str = str
    ls_len = len(load_str)

    animation = "|/-\\"
    anicount = 0

    i = 0

    while True:
        time.sleep(0.08)
        load_str_list = list(load_str)
        x = ord(load_str_list[i])
        y = 0

        if x != 32 and x != 46:
            if x>90:
                y = x-32
            else:
                y = x + 32
            load_str_list[i]= chr(y)

        res =''
        for j in range(ls_len):
            res = res + load_str_list[j]


        sys.stdout.write("\r"+res + animation[anicount])
        sys.stdout.flush()

        load_str = res

        anicount = (anicount + 1)% 4
        i =(i + 1)% ls_len


def zipExtract(zipfile, output):
    name = os.path.splitext(zipfile)
    if name[1] == ".zip" or name[1] == ".ZIP":
        os.mkdir(output)
        with ZipFile(zipfile, 'r') as zip:
            #zip.printdir()
            os.chdir(output)
            thread1 = threading.Thread(target = load_animation, args=("extracting your files",))
            thread1.start()
            #print(colored("Extracting your files..."))
            zip.extractall()
            print(colored("\nDone :)",'green'))
            os._exit(os.EX_OK)
    else:
        print(colored("Please provide a valid zip file", 'red'))
        sys.exit(2)

def get_all_file_paths(directory):
    file_paths = []
    for root, directories, files in os.walk(directory):
        for filename in files:
            filepath = os.path.join(root, filename)
            file_paths.append(filepath)
    return file_paths

def zipBind(directory):

    name = os.path.split(directory)
    file_paths = get_all_file_paths(directory)
    print(colored("Following files will be zipped: ",'yellow'))
    for file_name in file_paths:
        print(file_name)
    file_name = name[1]
    if file_name == '':
        file_name = "file"
    with ZipFile("{}.zip".format(file_name), 'w') as zip:
        thread1 = threading.Thread(target = load_animation, args=("generating zip files",))
        thread1.start()
        for file in file_paths:
            zip.write(file)

    print(colored('\nAll files zipped successfully :)', 'green'))
    os._exit(os.EX_OK)

def zipDetails(file):
    name = os.path.splitext(file)
    if name[1] == ".zip" or name[1] ==".ZIP":
        with ZipFile(file, 'r') as zip:
            for info in zip.infolist():
                print(info.filename)
                print("\tmodifies:\t" + str(datetime.datetime(*info.date_time)))
                print("\tSystem:\t\t" + str(info.create_system) +' (Windows = 0, Unix/Linux = 3)')
                print("\tZIP version:\t" + str(info.create_version))
                print("\tCompressed:\t" + str(info.compress_size/1024) + ' KB')
                print("\tUncompressed:\t" + str(info.file_size/1024) + ' KB')
    else:
        print(colored("Please provide a valid zip file",'red'))
        sys.exit(2)

def main():
    help = "Please Provide valid Option and file \nEx- ./zipy.py Options file \n-e : \"For Extracting a zip file\" \n-b : \"To create a zip file\" \n-d : \"To get the full details about the zip file\""
    if len(sys.argv) < 3:
        print("\033[1;32m{}".format(help))
        sys.exit(1)
    option = sys.argv[1]
    file = sys.argv[2]
    name = os.path.splitext(file)

    if option == "-e":
        zipThread = threading.Thread(target = zipExtract, args = (file,name[0],))
        zipThread.start()

    elif option == "-b":
        bindThread = threading.Thread(target = zipBind, args = (file,))
        bindThread.start()

    elif option == "-d":
        zipDetails(file)

    else:
        print(colored("{}".format(help), 'blue'))

if __name__ == '__main__':
    main()
