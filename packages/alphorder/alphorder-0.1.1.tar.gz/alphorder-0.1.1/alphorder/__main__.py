import os
import sys

from alphorder.sorter import Alphorder


def lengthAndDir(array, size, path):
    return len(array) == size and os.path.isdir(path)


def main():
    arguments = sys.argv
    if (len(arguments) > 1):
        path = arguments[1]
        if (os.path.isdir(path)):
            if(lengthAndDir(arguments, 2, path)):
                Alphorder.sort(path)
            elif(lengthAndDir(arguments, 3, path)):
                Alphorder.moveToFolder(path, sys.argv[2])
            elif(len(arguments) > 3 and os.path.isdir(path)):
                Alphorder.moveToFolderByKeywords(
                    path, sys.argv[2], sys.argv[3:])
        else:
            print('You have no specified a valid command')
    else:
        print('Path has not been specified: ',
              'alphorder path/to/folder')


if (__name__ == '__main__'):
    main()
