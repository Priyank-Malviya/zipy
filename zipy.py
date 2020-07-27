#!/usr/bin/env python3

from zipfile import ZipFile
import sys
import os
import datetime
from termcolor import colored
import time
import threading

# function create for console waiting animation
def load_animation(str):
    # string need to be print
    load_str = str
    ls_len = len(load_str)

    #animation string
    animation = "|/-\\"
    anicount = 0

    # variable to use index of the list of string
    i = 0

    while True:
        #speed of the animation the lower the value the faster the animation
        time.sleep(0.08)

        #convert the string to list to iterate over it
        load_str_list = list(load_str)
        x = ord(load_str_list[i])
        y = 0

        # used for making alphabets capital and smalls continuesly
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


# function used for extract zip file
def zipExtract(zipfile, output, verbose):
    try:
        # split the text of zip file to create a fiolder same as zip file name
        name = os.path.splitext(zipfile)

        #checking the format of file to valid the zip file
        if name[1] == ".zip" or name[1] == ".ZIP":
            os.mkdir(output)

            with ZipFile(zipfile, 'r') as zip:
                # used for change the directory to the created directory
                os.chdir(output)

                #checking the verbose is enable or not
                if verbose: zip.printdir()
                #create a thread to run the animation on the console
                thread1 = threading.Thread(target = load_animation, args=("extracting your files",))
                thread1.start()

                # extract all the files of zip file
                zip.extractall()
                print(colored("\nDone :)",'green'))

                #exit from the program entirely and stop the animation
                os._exit(os.EX_OK)
        else:
            print(colored("Please provide a valid zip file", 'red'))
            os._exit(os.EX_OK)

    except FileExistsError:
        print(colored("The directory that needs to be created its already Exists Please remove it and try again",'red'))
        sys.exit(2)

    except:
        print(colored("Please Provide a valid zip file",'red'))
        os.rmdir(output)
        sys.exit(2)

# this function returns all the files in a given directory so it can be compressed
def get_all_file_paths(directory):
    file_paths = []
    for root, directories, files in os.walk(directory):
        for filename in files:
            filepath = os.path.join(root, filename)
            file_paths.append(filepath)
    return file_paths

# function used for generate the zip file
def zipBind(directory, verbose):

    # checking the path so if it has / then it should remove
    name = os.path.splitext(directory)
    #print(name)

    #checking the file if it is not already zipped
    if name[1] != '.zip':
        if directory[-1] == "/":
            dir = directory[:-1]
        else: dir = directory

        # split the name to create the zip file
        name = os.path.split(dir)
        file_paths = get_all_file_paths(directory)

        # print the files in the directory
        if verbose:
            print(colored("Following files will be zipped: ",'yellow'))
            for file_name in file_paths:
                print(file_name)


        file_name = name[1]

        # create and open zip file in write mode
        with ZipFile("{}.zip".format(file_name), 'w') as zip:

            # create thread to start animation
            thread1 = threading.Thread(target = load_animation, args=("generating zip files",))
            thread1.start()

            # write all the files in a zip file
            for file in file_paths:
                zip.write(file)

        print(colored('\nAll files zipped successfully :) \"File Name: {}.zip\"'.format(file_name), 'green'))
        os._exit(os.EX_OK)
    else:
        print(colored("Please do not provide already zipped file",'red'))
        os._exit(os.EX_OK)

# function for showing all the details about files in a zip file
def zipDetails(file):
    name = os.path.splitext(file)

    # checking for valid zip file
    if name[1] == ".zip" or name[1] ==".ZIP":
        try:
            with ZipFile(file, 'r') as zip:
                for info in zip.infolist():
                    print(info.filename)
                    print("\tmodifies:\t" + str(datetime.datetime(*info.date_time)))
                    print("\tSystem:\t\t" + str(info.create_system) +' (Windows = 0, Unix/Linux = 3)')
                    print("\tZIP version:\t" + str(info.create_version))
                    print("\tCompressed:\t" + str(info.compress_size/1024) + ' KB')
                    print("\tUncompressed:\t" + str(info.file_size/1024) + ' KB')
        except:
            print(colored("Please Provide a Valid zip file",'red'))
    else:
        print(colored("Please provide a valid zip file",'red'))
        sys.exit(2)

# main function
def main():
    help = "Please Provide valid Option and file \nUsage- ./zipy.py Options file \n-e : \"For Extracting a zip file\" \n-b : \"To create a zip file\" \n-d : \"To get the full details about the zip file\" \n-v : \"Optional Parameter to get details(Please add verbose option at the last)\" \nEx- \t./zipy.py -b ~/example -v\n\t./zipy.py -e example.zip"
    if len(sys.argv) < 3:
        print("\033[1;32m{}".format(help))
        sys.exit(1)
    option = sys.argv[1]
    file = sys.argv[2]
    name = os.path.splitext(file)

    verbose_op = None
    verbose = False

    if len(sys.argv) == 4:
        verbose_op = sys.argv[3]

    if verbose_op == "-v":
        verbose = True
    if len(sys.argv) == 4 and verbose_op != "-v":
        print("\033[1;32m{}".format(help))
        sys.exit(1)

    if option == "-e":
        zipThread = threading.Thread(target = zipExtract, args = (file,name[0],verbose,))
        zipThread.start()

    elif option == "-b":
        bindThread = threading.Thread(target = zipBind, args = (file,verbose,))
        bindThread.start()

    elif option == "-d":
        zipDetails(file)

    else:
        print(colored("{}".format(help), 'blue'))

if __name__ == '__main__':
    main()
